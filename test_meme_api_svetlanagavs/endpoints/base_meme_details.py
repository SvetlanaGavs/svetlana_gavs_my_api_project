import allure
from test_meme_api_svetlanagavs.endpoints.base_endpoint import BaseEndpoint


class BaseMemeDetails(BaseEndpoint):
    @allure.step('Check id of the meme is correct')
    def check_id(self, meme_id):
        assert self.json['id'] == meme_id, (
            f'Expected id is {meme_id}, but got {self.json["id"]}.\n{self.curl}'
        )

    @allure.step('Check text of the meme is correct')
    def check_text(self, expected_text):
        assert self.json['text'] == expected_text, (
            f'Expected text is {expected_text}, but got {self.json["text"]}.\n{self.curl}'
        )

    @allure.step('Check url of the meme is correct')
    def check_url(self, expected_url):
        assert self.json['url'] == expected_url, (
            f'Expected url is {expected_url}, but got {self.json["url"]}.\n{self.curl}'
        )

    @allure.step('Check tags of the meme are correct')
    def check_tags(self, expected_tags):
        assert self.json['tags'] == expected_tags, (
            f'Expected tags are {expected_tags}, but got {self.json["tags"]}.\n{self.curl}'
        )

    @allure.step('Check info of the meme is correct')
    def check_info(self, expected_info):
        assert self.json['info'] == expected_info, (
            f'Expected info is {expected_info}, but got {self.json["info"]}.\n{self.curl}'
        )
