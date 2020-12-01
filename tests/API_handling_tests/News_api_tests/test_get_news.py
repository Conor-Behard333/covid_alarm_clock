from api_handling import get_news_info
from api_handling.get_news_info import get_news


def test_invalid_country_code():
    get_news_info.country = "england"
    assert get_news() is None


def test_valid_country_code():
    get_news_info.country = "gb"
    assert get_news() is not None


def test_valid_search_term():
    get_news_info.search_term = "Covid"
    assert get_news() is not None


def test_invalid_search_term():
    get_news_info.search_term = "this query shouldn't return any results"
    assert get_news() is None


def test_api_key():
    get_news_info.api_key = "298iewfg9d38gad"
    assert get_news() is None
