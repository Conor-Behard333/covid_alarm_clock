"""Handles retrieving and formatting the news data from the news api"""
import json
import requests
from api_handling.get_config_info import get_api_key, get_news_request_parameters
from flask import Markup
from random import choice
from logger_setup import setup_logger

log = setup_logger("News API.log", "log (news API)")

api_key = get_api_key("news_key")
country = get_news_request_parameters("country")
search_term = get_news_request_parameters("search_term")


def get_news() -> list:
    """Makes an api request to the news api

    :return: a list of top headlines
    """
    url_custom_top_headlines = f"country={country}&q={search_term}"
    url = f"http://newsapi.org/v2/top-headlines?{url_custom_top_headlines}" \
          f"&pageSize=100&apiKey={api_key}"

    response = requests.get(url).json()

    if response["status"] == "error":
        log.error(json.dumps(response, indent=4))
        response = None
    elif response["totalResults"] == 0:
        log.error("0 results found")
        response = None

    article_info = get_article_info(response)
    return article_info


def get_article_info(response: dict):
    """Create a list of articles containing the:
    Source name, title, description, url and author

    :param response:
    :return: a list of articles
    """
    article_info = []
    if response:
        for article_number in range(response["totalResults"]):
            source_name = response["articles"][article_number]["source"]["name"]
            title = response["articles"][article_number]["title"]
            description = response["articles"][article_number]["description"]
            url = response["articles"][article_number]["url"]
            article_info.append([title, description, url, source_name])
        return article_info
    return None


def get_news_formatted_for_notification() -> str:
    """Format the contents of a random article from the top headlines
    to then be displayed to the user on the web page.
    target="_blank" is used so that when the user clicks on the link a
    the article is opened on a new tab

    :return: The content to be displayed
    """
    articles = get_news()
    if articles:
        article = choice(articles)
        title = article[0]
        description = article[1]
        url = article[2]
        source = article[3]
        content = Markup(f"Title: {title}<br>"
                         f"Description: {description}<br>"
                         f"URL: <a target=\"_blank\" href=\"{url}\">CLICK ME</a> for more info<br>"
                         f"Source: {source}")
        return content
    return ""

