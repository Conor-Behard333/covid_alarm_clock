"""Handles retrieving and formatting the weather data from the weather api"""
import json
import requests
from api_handling.get_config_info import get_request_parameter
from logger_setup import setup_logger
from flask import Markup

log = setup_logger("Weather API.log", "log (weather API)")

api_key = get_request_parameter("API_keys", "weather_key")
country_code = get_request_parameter("Weather_API", "country")
city_name = get_request_parameter("Weather_API", "city_name")
units = get_request_parameter("Weather_API", "units")


def get_weather() -> dict:
    """Makes an api request for the weather api
    country code queries the specific country
    city name queries the specific city within that country
    units determines the type of numerical data returned (centigrade or Fahrenheit)

    :return: the response from the api
    """
    query = f"{city_name},{country_code}"
    url_current_weather = f"https://api.openweathermap.org/data/2.5/weather?q={query}" \
                          f"&appid={api_key}&units={units}"
    response = requests.get(url_current_weather).json()
    if response["cod"] != 200:
        log.error(json.dumps(response, indent=4))
        response = None
    return response


def get_weather_info() -> tuple:
    """grabs the description of the weather, temperature and what temperature it
    feels like from the json response from the weather api

    :return: what temperature it feels like, what the temperature is and the description
    of the weather
    """
    response = get_weather()
    if response:
        weather_description = response["weather"][0]["description"]
        temperature = str(response["main"]["temp"]) + u"\N{DEGREE SIGN}"
        feels_like = str(response["main"]["feels_like"]) + u"\N{DEGREE SIGN}"
        if units == "metric":
            temperature += "C"
            feels_like += "C"
        else:
            temperature += "F"
            feels_like += "F"
        return feels_like, temperature, weather_description
    return None, None, None


def get_weather_formatted_for_notification() -> str:
    """Format the data obtained from the weather api request

    :return: The content to be displayed
    """

    feels_like, temperature, weather_description = get_weather_info()
    if feels_like:
        content = Markup(f"Weather status: {weather_description}<br>"
                         f"Temperature: {temperature}<br>"
                         f"Feels like: {feels_like}")
        return content
    return ""
