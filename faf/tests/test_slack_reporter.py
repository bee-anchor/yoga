import faf.slack_reporter
import configparser
from unittest.mock import patch


class TestSlackReporter:

    test_config = configparser.ConfigParser()
    test_config.add_section('remote_service')
    test_config.set('remote_service', 'results_url', 'https://test_results.test')
    test_config.add_section('application')
    test_config.set('application', 'name', 'test')

    @patch('faf.slack_reporter.requests')
    @patch.object(faf.slack_reporter.Capabilities, 'get_formatted_remote_capabilities', lambda x: 'browserName: chrome, platform: Windows 10, version: 68.0')
    @patch('faf.slack_reporter.CONTEXT')
    def test_report_test_failure(self, mock_context, mock_requests):
        mock_context.config = self.test_config
        mock_context.driver.session_id = '1234'
        mock_context.args.environment = 'test'

        slack_reporter = faf.slack_reporter.SlackReporter("https://test_url.test")
        slack_reporter.report_test_failure()

        expected_payload = {
            "attachments": [
                {
                    "fallback": "Failed Test",
                    "pretext": "Failed Test",
                    "color": "#D00000",
                    "fields": [
                        {
                            "title": "APP: test, ENV: test",
                            "value": "DETAILS - browserName: chrome, platform: Windows 10, version: 68.0",
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
        mock_requests.post.assert_called_with("https://test_url.test",
                                                  json=expected_payload,
                                                  headers={'Content-Type': 'application/json'}
                                                  )


