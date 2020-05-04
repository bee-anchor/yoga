from pluggy.callers import _Result
from _pytest.reports import TestReport
import time
import os
from yoga.context import CONTEXT
from yoga.remote.sauce_helper import SauceHelper
from yoga.slack_reporter import SlackReporter
from yoga.aws import upload_screenshot_to_s3
from yoga.capabilities import Capabilities


class ConfTestHelper:

    def __init__(self):
        self.results = {}
        self.application = CONTEXT.config.get('application', 'name')
        self.s3_bucket = CONTEXT.config.get('remote_grid', 'remote_screenshot_s3_bucket')
        # If no aws keys or tokens are set, fallback to None, which will cause boto to use permissions on EC2 instance
        # set by it's IAM role
        self.aws_access_key = CONTEXT.config.get('environment', 'aws_ak', fallback=None)
        self.aws_secret_access_key = CONTEXT.config.get('environment', 'aws_sak', fallback=None)
        self.aws_session_token = CONTEXT.config.get('environment', 'aws_sak', fallback=None)

    def test_outcomes(self):
        return list(map(lambda result: result['outcome'], self.results.values()))

    def hook_pytest_runtest_makereport(self, outcome: _Result, item, call):
        # hook to handle actions to take when test outcomes are available
        rep: TestReport = outcome.get_result()

        if rep.head_line not in self.results.keys():
            self.results[rep.head_line] = {
                'outcome': None,
                's3_screenshot': None
            }

        if rep.when == 'call':
            self.results[rep.head_line]['outcome'] = rep.outcome

        if rep.outcome == 'failed':
            self._failed_test_item_action(rep, CONTEXT.args.execution)

    def hook_pytest_sessionfinish(self, session, exitstatus):
        if CONTEXT.args.execution in {'selenium_remote', 'appium_remote'}:
            self._report_outcome_to_sauce()
        if CONTEXT.args.slack_report and 'failed' in self.test_outcomes():
            self._report_outcome_to_slack()

    def _failed_test_item_action(self, rep: TestReport, execution_type: str) -> None:
        file_name = f"[{int(time.time())}][{rep.when}]{rep.head_line}.png"
        if execution_type in {'selenium_remote', 'appium_remote', 'grid_remote'}:
            try:
                self.results[rep.head_line]['s3_screenshot'] = upload_screenshot_to_s3(
                    CONTEXT.config.get('application', 'name') + '/' + file_name,
                    CONTEXT.driver.get_screenshot_as_png(),
                    CONTEXT.config.get('remote_grid', 'remote_screenshot_s3_bucket'),
                    CONTEXT.config.get('environment', 'aws_ak', fallback=None),
                    CONTEXT.config.get('environment', 'aws_sak', fallback=None),
                    CONTEXT.config.get('environment', 'aws_st', fallback=None)
                )
            except Exception as e:
                print('Failed to upload screenshot')
                print(e)
        elif execution_type in {'selenium_local', 'appium_local', 'grid_local'}:
            if not os.path.isdir('screenshots'):
                os.mkdir('screenshots')
            CONTEXT.driver.get_screenshot_as_file(f'screenshots/{rep.head_line}.png')

    def _report_outcome_to_sauce(self):
        if 'failed' in self.test_outcomes():
            SauceHelper().report_outcome(CONTEXT.driver.session_id, False)
        else:
            SauceHelper().report_outcome(CONTEXT.driver.session_id, True)

    def _report_outcome_to_slack(self):
        slack_reporter = SlackReporter(CONTEXT.config.get('slack', 'webhook'),
                                       CONTEXT.config.get('application', 'name'),
                                       CONTEXT.args.environment)
        failure_info = ""
        if CONTEXT.args.execution in {'selenium_remote', 'appium_remote'}:
            env_details = Capabilities(CONTEXT.args).get_formatted_remote_capabilities()
            failure_info = f"Sauce Results: {CONTEXT.config['remote_service']['results_url']}/{CONTEXT.driver.session_id}\n\n"
        elif CONTEXT.args.execution in {'appium_local'}:
            env_details = Capabilities(CONTEXT.args).get_formatted_local_capabilities()
        elif CONTEXT.args.execution != 'non-ui':
            env_details = CONTEXT.args.browser
        else:
            env_details = ""
        failure_info += "*Failed Tests:*\n"
        for test, info in self.results.items():
            if info['outcome'] == 'failed':
                failure_info += f"*_{test}_*\n"
                if info['s3_screenshot']:
                    failure_info += f"Screenshot: {info['s3_screenshot']}\n"
        slack_reporter.report_test_failure(env_details, failure_info)
