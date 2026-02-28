import requests
import curlify
import allure

from test_meme_api_svetlanagavs.endpoints.base_meme_details import BaseMemeDetails


class GetMeme(BaseMemeDetails):
    @allure.step('Get meme by id')
    def get_meme(self, meme_id, headers):
        self.response = requests.get(f'{self.base_url}/meme/{meme_id}', headers=headers)
        if self.response.status_code == 200:
            self.json = self.response.json()
        self.curl = curlify.to_curl(self.response.request)

        return self.response
