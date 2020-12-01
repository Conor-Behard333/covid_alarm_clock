"""Handles retrieving and formatting the covid data from the uk covid api """
from uk_covid19 import Cov19API
from flask import Markup
from api_handling.get_config_info import get_request_parameter

area_name = get_request_parameter("Covid_API", "areaName")


def get_covid_info() -> tuple:
    """Makes an api request to the covid 19 API, and retrieves the date, area, new cases
    and cumulative cases of each country in the UK

    :return: dictionary of data in json format
    """
    filters_for_local = [
        f"areaName={area_name}"
    ]

    filters_for_global = [
        "areaType=nation"
    ]

    data_to_retrieve = {
        "date": "date",
        "areaName": "areaName",
        "newCases": "newCasesByPublishDate",
        "totalCases": "cumCasesByPublishDate",
    }

    local_data = Cov19API(filters=filters_for_local, structure=data_to_retrieve, latest_by="date")
    uk_data = Cov19API(filters=filters_for_global, structure=data_to_retrieve, latest_by="date")

    local_data = local_data.get_json()
    uk_data = uk_data.get_json()
    return local_data, uk_data


def filter_data():
    """calculates the total uk cases and the total new cases in the UK
    and the total and new cases in the local area

    :return:the date, new case total and total cases in the UK, new cases and total cases
    local area
    """
    local_data, uk_data = get_covid_info()

    # get the date for the local data and uk data
    local_date = local_data["lastUpdate"].split("T")[0]
    uk_date = uk_data["lastUpdate"].split("T")[0]

    # get the new and total cases in the local area
    total_local_cases = local_data["data"][0]["totalCases"]
    local_new_cases = local_data["data"][0]["newCases"]

    # get the new and total cases in the UK
    total_uk_cases = 0
    total_new_cases = 0
    for area in uk_data["data"]:
        total_uk_cases += int(area["totalCases"])
        total_new_cases += int(area["newCases"])

    return local_date, uk_date, total_new_cases, total_uk_cases, local_new_cases, total_local_cases


def get_covid_info_formatted_for_notification():
    """Format the contents of the covid data to be displayed to the user
    on the web page.

    :return: The content to be displayed
    """
    local_date, uk_date, total_new_cases, total_uk_cases, local_new_cases, total_local_cases = filter_data()

    content = Markup(f"Total cases in the UK as of {uk_date}: {total_uk_cases}<br>"
                     f"Total cases in (location) as of {local_date}: {total_local_cases}<br>"
                     f"{total_new_cases} new cases today in the UK<br>"
                     f"{local_new_cases} new cases today in (location)")
    return content


def get_covid_info_formatted_for_announcement():
    """Format the data obtained from the covid api so that it can be announced
    to the user. \n allows the tts to pause after what has just been said.

    :return: The content to be announced
    """
    local_date, uk_date, total_new_cases, total_uk_cases, local_new_cases, total_local_cases = filter_data()

    content = f"Total cases in the UK as of {uk_date}: {total_uk_cases}\n" \
              f"Total cases in (location) as of {local_date}: {total_local_cases}\n" \
              f"{total_new_cases} new cases today in the UK\n" \
              f"{local_new_cases} new cases today in (location)"

    return content
