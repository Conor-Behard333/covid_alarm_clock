"""Handles retrieving and formatting the covid data from the uk covid api """
from uk_covid19 import Cov19API
from flask import Markup


def get_covid_info() -> dict:
    """Makes an api request to the covid 19 API, and retrieves the date, area, new cases
    and cumulative cases of each country in the UK

    :return: dictionary of data in json format
    """
    england_only = [
        "areaType=nation"
    ]

    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCases": "newCasesByPublishDate",
        "cumulativeCases": "cumCasesByPublishDate",
    }

    api = Cov19API(filters=england_only, structure=cases_and_deaths, latest_by="date")
    data = api.get_json()
    return data


def filter_data():
    """calculates the total uk cases and the total new cases in the UK

    :return:the date, new case total and total cases in the UK
    """
    data = get_covid_info()
    date = data["lastUpdate"].split("T")[0]
    total_uk_cases = 0
    total_new_cases = 0
    for area in data["data"]:
        total_uk_cases += int(area["cumulativeCases"])
        total_new_cases += int(area["newCases"])
    return date, total_new_cases, total_uk_cases


def get_covid_info_formatted_for_notification():
    """Format the contents of the covid data to be displayed to the user
    on the web page.

    :return: The content to be displayed
    """
    date, total_new_cases, total_uk_cases = filter_data()
    content = Markup(f"Total cases in the UK as of {date}: {total_uk_cases} <br>"
                     f"Total new cases for {date} in the UK: {total_new_cases}")
    return content


def get_covid_info_formatted_for_announcement():
    """Format the data obtained from the covid api so that it can be announced
    to the user. \n allows the tts to pause after what has just been said.

    :return: The content to be announced
    """
    date, total_new_cases, total_uk_cases = filter_data()
    content = f"Total cases in the UK as of {date}: {total_uk_cases}\n" \
              f"Total new cases for {date} in the UK: {total_new_cases}"

    return content
