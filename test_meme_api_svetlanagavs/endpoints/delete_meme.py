import requests
import curlify
import allure

from test_meme_api_svetlanagavs.endpoints.base_endpoint import BaseEndpoint


class DeleteMeme(BaseEndpoint):
    @allure.step('Delete meme')
    def delete_meme(self, meme_id, headers):
        self.response = requests.delete(f'{self.base_url}/meme/{meme_id}', headers=headers)
        self.text = self.response.text
        self.curl = curlify.to_curl(self.response.request)

        return self.response

    @allure.step('Check delete message is correct')
    def check_delete_message(self, meme_id):
        expected = f'Meme with id {meme_id} successfully deleted'
        assert expected in self.text, (
            f'Expected delete message containing "{expected}", but got {self.text}.\n{self.curl}'
        )
