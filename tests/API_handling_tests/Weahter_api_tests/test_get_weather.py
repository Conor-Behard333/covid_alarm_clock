from api_handling import get_weather_info
from api_handling.get_weather_info import get_weather


def test_invalid_country_code():
    get_weather_info.country_code = "r"
    assert get_weather() is None


def test_valid_country_code():
    get_weather_info.country_code = "gb"
    assert get_weather() is not None


def test_valid_city_name():
    get_weather_info.city_name = "exeter"
    assert get_weather() is not None


def test_invalid_city_name():
    get_weather_info.city_name = "This query should return none"
    assert get_weather() is None


def test_api_key():
    get_weather_info.api_key = "298iewfg9d38gad"
    assert get_weather() is None
