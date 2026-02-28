import requests
import curlify
import allure

from test_meme_api_svetlanagavs.endpoints.base_endpoint import BaseEndpoint


class GetAllMemes(BaseEndpoint):
    @allure.step('Get all memes')
    def get_all_memes(self, headers):
        self.response = requests.get(f'{self.base_url}/meme', headers=headers)
        if self.response.status_code == 200:
            self.json = self.response.json()
        self.curl = curlify.to_curl(self.response.request)

        return self.response

    @allure.step('Check meme is in the list')
    def check_meme_in_list(self, meme_id):
        meme_ids = [meme['id'] for meme in self.json['data']]
        assert meme_id in meme_ids, (
            f'Expected meme with id {meme_id} in the list, but it was not found.\n{self.curl}'
        )

    @allure.step('Check meme is not in the list')
    def check_meme_not_in_list(self, meme_id):
        meme_ids = [meme['id'] for meme in self.json['data']]
        assert meme_id not in meme_ids, (
            f'Expected meme with id {meme_id} not in the list, but it was found.\n{self.curl}'
        )
