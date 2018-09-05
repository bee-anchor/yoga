import requests
from faf.context import CONTEXT
from faf.capabilties import Capabilities

class SlackReporter:

    def __init__(self, webhook_url):
        self.url = webhook_url

    def report_test_failure(self):
        caps = Capabilities(CONTEXT.args).get_formatted_remote_capabilties()
        payload = {
           "attachments": [
              {
                 "fallback": "Failed Test",
                 "pretext": "Failed Test",
                 "color": "#D00000",
                 "fields": [
                    {
                       "title": f"APP: {CONTEXT.config['application']['name']}, ENV: {CONTEXT.args.environment}",
                       "value": f"DETAILS - {caps}",
                       "short": False
                    },
                    {
                       "title": "SauceLabs Results",
                       "value": f"{CONTEXT.config['remote_service']['results_url']}/{CONTEXT.driver.session_id}",
                       "short": False
                    }
                 ]
              }
           ]
        }
        return requests.post(self.url, json=payload, headers={'Content-Type': 'application/json'})
