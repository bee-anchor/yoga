from sauceclient import SauceClient
from faf.context import CONTEXT


class SauceHelper:

    def __init__(self):
        self.sauce_client = SauceClient(CONTEXT.config['remote_service']['username'], CONTEXT.config['remote_service']['access_key'])

    def report_outcome(self, test_passed):
        self.sauce_client.jobs.update_job(CONTEXT.driver.session_id, passed=test_passed)

    def update_job_name(self, name):
        self.sauce_client.jobs.update_job(CONTEXT.driver.session_id, name=name)

