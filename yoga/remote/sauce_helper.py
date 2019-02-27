import requests
from requests.auth import HTTPBasicAuth
from yoga.context import CONTEXT


class SauceHelper:

    def __init__(self):
        self.rest_api = CONTEXT.config.get('remote_service', 'api_url', fallback="https://saucelabs.com/rest")
        self.username = CONTEXT.config.get('remote_service', 'username')
        self.access_key = CONTEXT.config.get('remote_service', 'access_key')
        self.headers = {'Content-Type': 'application/json'}

    def auth(self):
        """Create auth string from credentials."""
        return HTTPBasicAuth(self.username, self.access_key)

    def report_outcome(self, session_id, test_passed):
        url = self.rest_api + f"/v1/{self.username}/jobs/{session_id}"
        body = {"passed": test_passed}
        requests.put(url, json=body, headers=self.headers, auth=self.auth())

    def update_job_name(self, session_id, name):
        url = self.rest_api + f"/v1/{self.username}/jobs/{session_id}"
        body = {"name": name}
        requests.put(url, json=body, headers=self.headers, auth=self.auth())

