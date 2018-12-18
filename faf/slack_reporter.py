import requests
from faf.context import CONTEXT

class SlackReporter:

    def __init__(self, webhook_url):
        self.url = webhook_url

    def report_test_failure(self, caps_or_browser, failure_info):
        payload = {
           "attachments": [
              {
                 "fallback": "Failed Test",
                 "pretext": "Failed Test",
                 "color": "#D00000",
                 "fields": [
                    {
                       "title": f"APP: {CONTEXT.config['application']['name']}, ENV: {CONTEXT.args.environment}",
                       "value": f"DETAILS - {caps_or_browser}",
                       "short": False
                    },
                    {
                       "title": "Failure Info",
                       "value": failure_info,
                       "short": False
                    }
                 ]
              }
           ]
        }
        return requests.post(self.url, json=payload, headers={'Content-Type': 'application/json'})
