import requests
import curlify
import allure

from test_meme_api_svetlanagavs.endpoints.base_endpoint import BaseEndpoint


class Authorize(BaseEndpoint):
    @allure.step('Authorize user')
    def authorize(self, name):
        payload = {"name": name}
        self.response = requests.post(f'{self.base_url}/authorize', json=payload)
        self.json = self.response.json()
        self.curl = curlify.to_curl(self.response.request)
        return self.json.get('token')

    @allure.step('Check token is not None')
    def check_token_is_not_none(self, token):
        assert token is not None, f'Expected token, but got None.\n{self.curl}'
