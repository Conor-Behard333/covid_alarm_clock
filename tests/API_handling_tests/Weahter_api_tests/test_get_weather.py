from api_handling import get_weather_info
from api_handling.get_weather_info import get_weather


def test_1():
    get_weather_info.country_code = "r"
    assert get_weather() is None


def test_3():
    get_weather_info.country_code = "gb"
    assert get_weather() is not None


def test_4():
    get_weather_info.city_name = "exeter"
    assert get_weather() is not None


def test_5():
    get_weather_info.city_name = "This query should return none"
    assert get_weather() is None


def test_6():
    get_weather_info.api_key = "298iewfg9d38gad"
    assert get_weather() is None
