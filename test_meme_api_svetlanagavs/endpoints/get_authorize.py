import os
import requests
import curlify
import allure

from test_meme_api_svetlanagavs.endpoints.base_endpoint import BaseEndpoint
from test_meme_api_svetlanagavs.endpoints.post_authorize import Authorize


class CheckToken(BaseEndpoint):
    @allure.step('Check if token is alive')
    def check_token_is_alive(self, token):
        self.response = requests.get(f'{self.base_url}/authorize/{token}')
        self.curl = curlify.to_curl(self.response.request)
        return self.response.status_code == 200

    @allure.step('Check token is alive')
    def check_token_alive(self, token):
        result = self.check_token_is_alive(token)
        assert result is True, f'Expected token to be alive, but it is not.\n{self.curl}'

    @allure.step('Check token is not alive')
    def check_token_not_alive(self, token):
        result = self.check_token_is_alive(token)
        assert result is False, f'Expected token to be dead, but it is alive.\n{self.curl}'


def get_token(name='svetlana_gavs'):
    saved_token = os.environ.get('MEME_API_TOKEN')
    if saved_token and CheckToken().check_token_is_alive(saved_token):
        return saved_token

    token = Authorize().authorize(name)
    os.environ['MEME_API_TOKEN'] = token
    return token
