import requests
import curlify
import allure

from test_meme_api_svetlanagavs.endpoints.base_meme_details import BaseMemeDetails


class UpdateMeme(BaseMemeDetails):
    @allure.step('Update meme')
    def update_meme(self, meme_id, payload, headers):
        self.response = requests.put(f'{self.base_url}/meme/{meme_id}', json=payload, headers=headers)
        if self.response.status_code == 200:
            self.json = self.response.json()
        self.curl = curlify.to_curl(self.response.request)

        return self.response
