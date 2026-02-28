import pytest

from test_meme_api_svetlanagavs.endpoints import post_authorize
from test_meme_api_svetlanagavs.endpoints import get_authorize
from test_meme_api_svetlanagavs.endpoints import post_meme
from test_meme_api_svetlanagavs.endpoints import get_all_memes
from test_meme_api_svetlanagavs.endpoints import get_meme
from test_meme_api_svetlanagavs.endpoints import put_meme
from test_meme_api_svetlanagavs.endpoints import delete_meme


@pytest.fixture(scope='session')
def auth_headers():
    token = get_authorize.get_token()
    return {"Authorization": token}


@pytest.fixture()
def post_authorize_ep():
    return post_authorize.Authorize()


@pytest.fixture()
def get_authorize_ep():
    return get_authorize.CheckToken()


@pytest.fixture()
def post_meme_ep():
    return post_meme.CreateMeme()


@pytest.fixture()
def get_all_memes_ep():
    return get_all_memes.GetAllMemes()


@pytest.fixture()
def get_meme_ep():
    return get_meme.GetMeme()


@pytest.fixture()
def put_meme_ep():
    return put_meme.UpdateMeme()


@pytest.fixture()
def delete_meme_ep():
    return delete_meme.DeleteMeme()


@pytest.fixture()
def create_and_delete_meme(request, auth_headers, post_meme_ep, delete_meme_ep):
    text, url, tags, info = request.param

    post_meme_ep.create_meme(text, url, tags, info, auth_headers)
    meme_id = post_meme_ep.json['id']

    yield post_meme_ep

    delete_meme_ep.delete_meme(meme_id, auth_headers)
