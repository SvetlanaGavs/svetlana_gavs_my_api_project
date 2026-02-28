# Meme API Test Suite

Automated API tests for [Meme API](http://memesapi.course.qa-practice.com).

## Tech Stack

- Python 3.12
- pytest
- requests
- Allure

## Project Structure

```
test_meme_api_svetlanagavs/
├── endpoints/                # API endpoint classes
│   ├── base_endpoint.py      # base class with common checks
│   ├── base_meme_details.py  # base class for meme field checks
│   ├── post_authorize.py     # POST /authorize
│   ├── get_authorize.py      # GET /authorize/{token}
│   ├── post_meme.py          # POST /meme
│   ├── get_meme.py           # GET /meme/{id}
│   ├── get_all_memes.py      # GET /meme
│   ├── put_meme.py           # PUT /meme/{id}
│   └── delete_meme.py        # DELETE /meme/{id}
├── tests/
│   ├── test_data.py          # test data constants
│   └── test_meme.py          # test cases
└── conftest.py               # fixtures
```

## Setup

```bash
pip install -r requirements.txt
```

## Run Tests

```bash
pytest
```

With Allure report:

```bash
pytest --alluredir=allure-results
allure serve allure-results
```
