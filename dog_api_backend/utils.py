from pytz import timezone
from datetime import datetime
from flask import current_app


def get_now_in_tz():
    timezone_str = current_app.config.get("TIMEZONE")
    return datetime.now(timezone(timezone_str))


def set_time_in_payload(dict_user):
    """Sets the time with today and minutes in the payload"""
    current_date = get_now_in_tz()
    dict_user["today"] = current_date.strftime("%Y-%m-%d")
    dict_user["hours"] = current_date.strftime("%H:%M")