import requests
import curlify
import allure

from test_meme_api_svetlanagavs.endpoints.base_meme_details import BaseMemeDetails


class CreateMeme(BaseMemeDetails):
    @allure.step('Create a new meme')
    def create_meme(self, text, url, tags, info, headers):
        payload = {
            "text": text,
            "url": url,
            "tags": tags,
            "info": info
        }
        self.response = requests.post(f'{self.base_url}/meme', json=payload, headers=headers)
        if self.response.status_code == 200:
            self.json = self.response.json()
        self.curl = curlify.to_curl(self.response.request)

        return self.response
