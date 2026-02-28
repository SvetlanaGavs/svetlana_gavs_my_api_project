import pytest

from test_meme_api_svetlanagavs.tests.test_data import MEME_TEXT, MEME_URL, MEME_TAGS, MEME_INFO

"""
AUTHORIZE (3 tests):
  - Authorization returns a token
  - Valid token is alive
  - Invalid token is not alive
"""


def test_authorize(post_authorize_ep):
    token = post_authorize_ep.authorize('test_user')
    post_authorize_ep.check_status_code()
    post_authorize_ep.check_token_is_not_none(token)


def test_token_is_alive(auth_headers, get_authorize_ep):
    token = auth_headers['Authorization']
    get_authorize_ep.check_token_alive(token)


def test_invalid_token_is_not_alive(get_authorize_ep):
    get_authorize_ep.check_token_not_alive('invalid_token_123')


"""
CREATE MEME (5 tests):
  - Create meme with valid payloads (2 variants)
  - Response data is correct
  - Created meme is actually saved (verified via GET)
  - Without authorization -> 401
  - With missing required fields -> 400
"""


@pytest.mark.parametrize(
    'create_and_delete_meme',
    [
        (MEME_TEXT, MEME_URL, MEME_TAGS, MEME_INFO),
        ('Another meme', 'https://example.com/meme2.jpg', ['sad', 'test'], {'author': 'bot', 'year': 2025}),
    ],
    indirect=True
)
def test_create_meme(create_and_delete_meme):
    created_meme = create_and_delete_meme

    created_meme.check_status_code(200)
    created_meme.check_instance(dict)
    created_meme.check_response_is_not_empty()


@pytest.mark.parametrize(
    'create_and_delete_meme',
    [(MEME_TEXT, MEME_URL, MEME_TAGS, MEME_INFO)],
    indirect=True
)
def test_create_meme_has_correct_data(create_and_delete_meme):
    created_meme = create_and_delete_meme

    created_meme.check_text(MEME_TEXT)
    created_meme.check_url(MEME_URL)
    created_meme.check_tags(MEME_TAGS)
    created_meme.check_info(MEME_INFO)


def test_create_meme_without_auth(post_meme_ep):
    post_meme_ep.create_meme(MEME_TEXT, MEME_URL, MEME_TAGS, MEME_INFO, headers={})
    post_meme_ep.check_status_code(401)


@pytest.mark.parametrize(
    'create_and_delete_meme',
    [(MEME_TEXT, MEME_URL, MEME_TAGS, MEME_INFO)],
    indirect=True
)
def test_created_meme_is_saved(create_and_delete_meme, auth_headers, get_meme_ep):
    created_meme = create_and_delete_meme
    meme_id = created_meme.json['id']

    get_meme_ep.get_meme(meme_id, auth_headers)
    get_meme_ep.check_status_code()
    get_meme_ep.check_text(MEME_TEXT)
    get_meme_ep.check_url(MEME_URL)
    get_meme_ep.check_tags(MEME_TAGS)
    get_meme_ep.check_info(MEME_INFO)


def test_create_meme_with_missing_fields(auth_headers, post_meme_ep):
    post_meme_ep.create_meme('only text', None, None, None, auth_headers)
    post_meme_ep.check_status_code(400)


"""
GET ALL MEMES (3 tests):
  - Get list of all memes
  - Created meme appears in the list
  - Without authorization -> 401
"""


def test_get_all_memes(auth_headers, get_all_memes_ep):
    get_all_memes_ep.get_all_memes(auth_headers)

    get_all_memes_ep.check_status_code()
    get_all_memes_ep.check_instance(dict)


@pytest.mark.parametrize(
    'create_and_delete_meme',
    [(MEME_TEXT, MEME_URL, MEME_TAGS, MEME_INFO)],
    indirect=True
)
def test_created_meme_appears_in_list(create_and_delete_meme, auth_headers, get_all_memes_ep):
    created_meme = create_and_delete_meme
    meme_id = created_meme.json['id']

    get_all_memes_ep.get_all_memes(auth_headers)
    get_all_memes_ep.check_status_code()
    get_all_memes_ep.check_meme_in_list(meme_id)


def test_get_all_memes_without_auth(get_all_memes_ep):
    get_all_memes_ep.get_all_memes(headers={})
    get_all_memes_ep.check_status_code(401)


"""
GET MEME BY ID (2 tests):
  - Get meme by id with all fields verified
  - Nonexistent meme -> 404
"""


@pytest.mark.parametrize(
    'create_and_delete_meme',
    [(MEME_TEXT, MEME_URL, MEME_TAGS, MEME_INFO)],
    indirect=True
)
def test_get_meme_by_id(create_and_delete_meme, auth_headers, get_meme_ep):
    created_meme = create_and_delete_meme
    meme_id = created_meme.json['id']

    get_meme_ep.get_meme(meme_id, auth_headers)

    get_meme_ep.check_status_code()
    get_meme_ep.check_id(meme_id)
    get_meme_ep.check_text(MEME_TEXT)
    get_meme_ep.check_url(MEME_URL)
    get_meme_ep.check_tags(MEME_TAGS)
    get_meme_ep.check_info(MEME_INFO)


def test_get_nonexistent_meme(auth_headers, get_meme_ep):
    get_meme_ep.get_meme(999999, auth_headers)
    get_meme_ep.check_status_code(404)


"""
UPDATE MEME (4 tests):
  - Update meme + verify via GET
  - Second update overwrites the first one
  - Nonexistent meme -> 404
  - Without authorization -> 401
"""


@pytest.mark.parametrize(
    'create_and_delete_meme',
    [(MEME_TEXT, MEME_URL, MEME_TAGS, MEME_INFO)],
    indirect=True
)
def test_update_meme(create_and_delete_meme, auth_headers, put_meme_ep, get_meme_ep):
    created_meme = create_and_delete_meme
    meme_id = created_meme.json['id']

    updated_payload = {
        "id": meme_id,
        "text": "Updated meme text",
        "url": "https://example.com/updated.jpg",
        "tags": ["updated", "test"],
        "info": {"author": "svetlana", "year": 2025}
    }

    put_meme_ep.update_meme(meme_id, updated_payload, auth_headers)
    put_meme_ep.check_status_code()
    put_meme_ep.check_text("Updated meme text")
    put_meme_ep.check_url("https://example.com/updated.jpg")
    put_meme_ep.check_tags(["updated", "test"])
    put_meme_ep.check_info({"author": "svetlana", "year": 2025})

    get_meme_ep.get_meme(meme_id, auth_headers)
    get_meme_ep.check_status_code()
    get_meme_ep.check_text("Updated meme text")


@pytest.mark.parametrize(
    'create_and_delete_meme',
    [(MEME_TEXT, MEME_URL, MEME_TAGS, MEME_INFO)],
    indirect=True
)
def test_update_meme_twice(create_and_delete_meme, auth_headers, put_meme_ep, get_meme_ep):
    created_meme = create_and_delete_meme
    meme_id = created_meme.json['id']

    first_payload = {
        "id": meme_id,
        "text": "First update",
        "url": "https://example.com/first.jpg",
        "tags": ["first"],
        "info": {"version": 1}
    }
    put_meme_ep.update_meme(meme_id, first_payload, auth_headers)
    put_meme_ep.check_status_code()

    second_payload = {
        "id": meme_id,
        "text": "Second update",
        "url": "https://example.com/second.jpg",
        "tags": ["second"],
        "info": {"version": 2}
    }
    put_meme_ep.update_meme(meme_id, second_payload, auth_headers)
    put_meme_ep.check_status_code()

    get_meme_ep.get_meme(meme_id, auth_headers)
    get_meme_ep.check_status_code()
    get_meme_ep.check_text("Second update")
    get_meme_ep.check_url("https://example.com/second.jpg")
    get_meme_ep.check_tags(["second"])
    get_meme_ep.check_info({"version": 2})


def test_update_nonexistent_meme(auth_headers, put_meme_ep):
    payload = {
        "id": 999999,
        "text": "ghost",
        "url": "https://example.com/ghost.jpg",
        "tags": ["ghost"],
        "info": {"author": "nobody"}
    }
    put_meme_ep.update_meme(999999, payload, auth_headers)
    put_meme_ep.check_status_code(404)


def test_update_meme_without_auth(put_meme_ep):
    payload = {
        "id": 1,
        "text": "hack",
        "url": "https://example.com/hack.jpg",
        "tags": ["hack"],
        "info": {"author": "hacker"}
    }
    put_meme_ep.update_meme(1, payload, headers={})
    put_meme_ep.check_status_code(401)


"""
DELETE MEME (4 tests):
  - Delete meme + verify 404 on GET
  - Deleted meme disappears from the list
  - Delete already deleted meme -> 404
  - Without authorization -> 401
"""


@pytest.mark.parametrize(
    'create_and_delete_meme',
    [(MEME_TEXT, MEME_URL, MEME_TAGS, MEME_INFO)],
    indirect=True
)
def test_delete_meme(create_and_delete_meme, auth_headers, delete_meme_ep, get_meme_ep):
    created_meme = create_and_delete_meme
    meme_id = created_meme.json['id']

    delete_meme_ep.delete_meme(meme_id, auth_headers)
    delete_meme_ep.check_status_code()
    delete_meme_ep.check_delete_message(meme_id)

    get_meme_ep.get_meme(meme_id, auth_headers)
    get_meme_ep.check_status_code(404)


@pytest.mark.parametrize(
    'create_and_delete_meme',
    [(MEME_TEXT, MEME_URL, MEME_TAGS, MEME_INFO)],
    indirect=True
)
def test_deleted_meme_not_in_list(create_and_delete_meme, auth_headers, delete_meme_ep, get_all_memes_ep):
    created_meme = create_and_delete_meme
    meme_id = created_meme.json['id']

    delete_meme_ep.delete_meme(meme_id, auth_headers)
    delete_meme_ep.check_status_code()

    get_all_memes_ep.get_all_memes(auth_headers)
    get_all_memes_ep.check_meme_not_in_list(meme_id)


def test_delete_already_deleted_meme(auth_headers, post_meme_ep, delete_meme_ep):
    post_meme_ep.create_meme(MEME_TEXT, MEME_URL, MEME_TAGS, MEME_INFO, auth_headers)
    meme_id = post_meme_ep.json['id']

    delete_meme_ep.delete_meme(meme_id, auth_headers)
    delete_meme_ep.check_status_code()

    delete_meme_ep.delete_meme(meme_id, auth_headers)
    delete_meme_ep.check_status_code(404)


def test_delete_meme_without_auth(delete_meme_ep):
    delete_meme_ep.delete_meme(1, headers={})
    delete_meme_ep.check_status_code(401)
