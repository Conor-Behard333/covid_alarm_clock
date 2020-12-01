"""Handles retrieving the data from the config file"""
import json
from logger_setup import setup_logger

config_file = json.load(open("config.json"))

log = setup_logger("Config File.log", "log (config)")


def get_request_parameter(first_key: str, second_key: str) -> str:
    """Gets a value from the json file given the first and second key

    :param first_key: holds the first key for the json file
    :param second_key: holds the first second key for the json file
    :return: the value from the json file
    """
    try:
        item = config_file[first_key][second_key]
    except KeyError:
        item = None
        log.error("%s,  %s does not exist", first_key, second_key)
    return item
