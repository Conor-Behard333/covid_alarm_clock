"""Handles retrieving the data from the config file"""
import json

config_file = json.load(open("config.json"))


def get_api_key(key_name: str) -> str:
    """Gets the specified api key from the config file

    :param key_name: name of the api key (weather or news)
    :return: api key
    """
    return config_file["API_keys"][key_name]


def get_news_request_parameters(item_name: str) -> str:
    """Gets the specified api request parameters from the news api from the config file

    :param item_name: name of the api parameter
    :return: parameter for the api request
    """
    return config_file["News_API"][item_name]


def get_weather_request_parameters(item_name: str) -> str:
    """Gets the specified api details for the weather api from the config file

    :param item_name: name of the api parameter
    :return: parameter for the api request
    """
    return config_file["Weather_API"][item_name]
