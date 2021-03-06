import requests


class SlackReporter:

    def __init__(self, webhook_url: str, app_name: str, env: str):
        self.url = webhook_url
        self.app_name = app_name
        self.env = env

    def report_test_failure(self, caps_or_browser: str, failure_info: str):
        payload = {
            "attachments": [
                {
                    "fallback": "Failed Test",
                    "pretext": "Failed Test",
                    "color": "#D00000",
                    "fields": [
                        {
                            "title": f"APP: {self.app_name}, DETAILS: env: {self.env} {caps_or_browser}",
                            "short": False
                        },
                        {
                            "value": failure_info,
                            "short": False
                        }
                    ]
                }
            ]
        }
        return requests.post(self.url, json=payload, headers={'Content-Type': 'application/json'})
