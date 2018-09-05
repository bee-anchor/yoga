import faf.slack_reporter
import configparser
import pytest
from unittest.mock import MagicMock

class TestSlackReporter:

    request_post_mock = MagicMock()
    faf.slack_reporter.requests.post = request_post_mock

    caps = str({'browserName': 'chrome', 'platform': 'Windows 10', 'version': '68.0'})
    remote_caps_mock = MagicMock(
        return_value=caps
    )
    faf.slack_reporter.Capabilities.get_remote_capabilities = remote_caps_mock

    test_config = configparser.ConfigParser()
    test_config.add_section('remote_service')
    test_config.set('remote_service', 'results_url', 'https://test_results.test')
    test_config.add_section('application')
    test_config.set('application', 'name', 'test')
    faf.slack_reporter.CONTEXT.config = test_config
    faf.slack_reporter.CONTEXT.driver.session_id = '1234'

    slack_reporter = faf.slack_reporter.SlackReporter("https://test_url.test")

    def test_report_test_failure(self):
        self.slack_reporter.report_test_failure()

        expected_payload = {
           "attachments": [
              {
                 "fallback": "Failed Test",
                 "pretext": "Failed Test",
                 "color": "#D00000",
                 "fields": [
                    {
                       "title": 'test',
                       "value": "Details: {'browserName': 'chrome', 'platform': 'Windows 10', 'version': '68.0'}",
                       "short": False
                    },
                    {
                       "title": "SauceLabs Results",
                       "value": "https://test_results.test/1234",
                       "short": False
                    }
                 ]
              }
           ]
        }
        self.request_post_mock.assert_called_with("https://test_url.test",
                                                  json=expected_payload,
                                                  headers={'Content-Type': 'application/json'}
                                                  )


