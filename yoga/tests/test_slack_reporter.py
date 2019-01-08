import yoga.slack_reporter
import configparser
from unittest.mock import patch


class TestSlackReporter:

    @patch('yoga.slack_reporter.requests')
    def test_report_test_failure(self, mock_requests):
        slack_reporter = yoga.slack_reporter.SlackReporter("https://test_url.test", 'test', 'test')
        slack_reporter.report_test_failure('chrome', 'failed')

        expected_payload = {
            "attachments": [
                {
                    "fallback": "Failed Test",
                    "pretext": "Failed Test",
                    "color": "#D00000",
                    "fields": [
                        {
                            "title": "APP: test, ENV: test",
                            "value": "DETAILS - chrome",
                            "short": False
                        },
                        {
                            "title": "Failure Info",
                            "value": "failed",
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
