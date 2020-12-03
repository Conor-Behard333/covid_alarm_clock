"""Main module responsible for handling updates from flask,
setting and displaying alarms and announcing notifications
"""
from datetime import date, datetime
import sched
import time
import pyttsx3

from flask import Flask, render_template, request, Markup
from logger_setup import setup_logger
from api_handling.get_weather_info import get_weather_formatted_for_notification
from api_handling.get_news_info import get_news_formatted_for_notification
from api_handling.get_covid_info import get_covid_info_formatted_for_notification, \
    get_covid_info_formatted_for_announcement

# create a scheduler object for adding notifications
notification_scheduler = sched.scheduler(time.time, time.sleep)

# create a scheduler object for adding notifications
announcement_scheduler = sched.scheduler(time.time, time.sleep)

# create a flask app
app = Flask(__name__)

alarms = []
notifications = []
announcements = []
log = setup_logger("Main.log", "log")


def announce():
    """Use text to speech to announce notifications

    :return: None
    """
    if len(announcements) > 0:
        try:
            tts = pyttsx3.init()
            tts.setProperty("volume", 0.5)
            for announcement in announcements:
                tts.say(announcement)

            log.info("notifications are being announced")
            tts.runAndWait()
            del tts
            log.info("notifications are no longer being announced")
            announcements.clear()
        except RuntimeError as error:
            announcements.clear()
            log.error("ERROR %s", error)


def add_covid_notification():
    """adds a news notification to the notification list
    and adds an announcement for the tts to say for covid notifications

    :return: None
    """
    covid_content = get_covid_info_formatted_for_notification()
    current_time = datetime.now().strftime("%H:%M")
    notification = {"title": f"Covid update for {current_time}", "content": covid_content}
    notifications.append(notification)
    announcements.append(get_covid_info_formatted_for_announcement())
    log.info("Covid update notification has been added")


def add_news_notification():
    """adds a news notification to the notification list
    and adds an announcement for the tts to say for news notifications

    :return: None
    """
    news_content = get_news_formatted_for_notification()
    if news_content != "":
        current_time = datetime.now().strftime("%H:%M")
        notification = {"title": f"News Briefing for {current_time}", "content": news_content}
        notifications.append(notification)
        log.info("News Briefing notification has been added")
    else:
        log.error("Notification was not added as there was a problem with the API. "
                  "See News API.log for more information")


def add_weather_notification():
    """adds a weather notification to the notification list
    and adds an announcement for the tts to say for weather notifications

    :return: None
    """
    weather_content = get_weather_formatted_for_notification()
    if weather_content:
        current_time = datetime.now().strftime("%H:%M")
        notification = {"title": f"Weather Briefing for {current_time}", "content": weather_content}
        notifications.append(notification)
        log.info("Weather Briefing notification has been added")
    else:
        log.error("Notification was not added as there was a problem with the API. "
                  "See Weather API.log for more information")


def delete_alarm(alarm_title: str):
    """removes the alarm with the given title

    :param alarm_title: the title of the alarm being removed
    :return: None
    """
    for alarm in alarms:
        if alarm["title"] == alarm_title:
            alarms.remove(alarm)
            log.info("%s alarm has been removed", alarm_title)


def delete_notification(notification_title: str):
    """removes the notification with the given title

    :param notification_title: the title of the notification being removed
    :return: None
    """
    for notification in notifications:
        if notification["title"] == notification_title:
            notifications.remove(notification)
            log.info("%s notification has been removed", notification_title)


def set_off_alarms(alarm: dict):
    """sets off the alarm passed into the function.
    adds a covid notification and announcement
    adds a weather/news notification if it has been selected

    :param alarm: the alarm that is being set off
    :return:
    """
    # only sets off alarm if it is in the alarm list
    if alarm in alarms:
        alarms.remove(alarm)  # delete alarm
        log.info("%s alarm has been removed", alarm["title"])
        add_covid_notification()
        if alarm["news"]:
            add_news_notification()
        if alarm["weather"]:
            add_weather_notification()
        announcement_scheduler.enterabs(0, 1, announce)
        announcement_scheduler.run(blocking=False)
    else:
        log.info("No alarm was found")


def check_for_delete_request():
    """Check to see if the user has attempted to delete a notification or alarm
    if they have then remove that alarm/notification
    :return: None
    """
    alarm_title_delete = request.args.get("alarm_item")
    notification_title_delete = request.args.get("notif")
    if alarm_title_delete:
        delete_alarm(alarm_title_delete)
    if notification_title_delete:
        delete_notification(notification_title_delete)


def get_notification_delay(alarm_time_date: str) -> int:
    """Calculates the amount of time (in seconds) that the scheduler should be
    delayed for, for adding the notification

    :param alarm_time_date: The time and date set for the alarm
    :return: the time delay in seconds
    """
    alarm_date = alarm_time_date.split("T")[0].split("-")
    alarm_time = alarm_time_date.split("T")[1].split(":")

    current_date = date.today().strftime("%Y-%m-%d").split("-")
    current_time = datetime.now().strftime("%H:%M").split(":")

    current_date_time = datetime(int(current_date[0]), int(current_date[1]), int(current_date[2]),
                                 int(current_time[0]), int(current_time[1]))

    alarm_date_time = datetime(int(alarm_date[0]), int(alarm_date[1]), int(alarm_date[2]),
                               int(alarm_time[0]), int(alarm_time[1]))
    time_difference = alarm_date_time - current_date_time
    delay = int(time_difference.total_seconds())
    return delay


def valid_alarm_title(alarm_title: str) -> bool:
    """checks to see if there are any alarms that currently exist with the same name
    as the alarm the user wants to add

    :param alarm_title: name of the alarm
    :return: True if it is a valid alarm, False if it is not
    """
    for alarm in alarms:
        if alarm["title"] == alarm_title:
            log.info("Invalid alarm name %s as one already exits", alarm_title)
            return False
    return True


@app.route('/')
@app.route('/index')
def index():
    """Every time the html page refreshes this function is called.
    Checks for any activity from the user (setting an alarm, deleting an alarm,
    or deleting a notification)

    :return: The html template with alarms and notifications added
    """
    notification_scheduler.run(blocking=False)

    # get the inputs from the users alarm submission
    alarm_time = request.args.get("alarm")
    alarm_title = request.args.get("two")
    alarm_news = request.args.get("news")
    alarm_weather = request.args.get("weather")
    check_for_delete_request()

    if alarm_title and alarm_time:
        alarm = {"alarm time": str(alarm_time), "title": str(alarm_title), "content": "",
                 "weather": alarm_weather is not None, "news": alarm_news is not None}

        notification_delay = get_notification_delay(alarm["alarm time"])

        # if the notification delays is negative then it is set in the past which is invalid
        if notification_delay > 0 and valid_alarm_title(alarm["title"]):
            alarm_date_time = alarm_time.split("T")

            alarm["content"] = format_alarm_content(alarm_date_time, alarm_news, alarm_weather)

            notification_scheduler.enter(notification_delay, len(notifications),
                                         set_off_alarms, (alarm,))

            log.info("Alarm set: %s", alarm)
            log.info("Delay for alarm: %d seconds", notification_delay)
            alarms.append(alarm)
        else:
            log.error("INVALID ALARM: %s", alarm)

    return render_template('index.html', title='Daily update', alarms=alarms,
                           notifications=notifications, image="alarm_clock.jpg",
                           favicon="static/images/favicon.jpg")


def format_alarm_content(alarm_date_time: list, alarm_news: bool, alarm_weather: bool) -> str:
    """Formats the content displayed in the contents container of the alarm

    :param alarm_date_time: date and time set for the alarm
    :param alarm_news: True if the user has selected the news checkbox
    :param alarm_weather: True if the user has selected the weather checkbox
    :return:
    """
    content = Markup(f"Date set for {alarm_date_time[0]}<br>"
                     f"Time set for {alarm_date_time[1]}<br>")
    if alarm_weather:
        content += Markup("Weather briefing included<br>")
    if alarm_news:
        content += "News briefing included"
    return content


if __name__ == '__main__':
    app.run()
