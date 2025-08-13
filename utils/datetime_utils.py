# AstroAgent/utils/datetime_utils.py

from datetime import datetime, timedelta

def parse_datetime(date_str, time_str):
    """Convert date and time strings into a datetime object"""
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

def days_between(date1, date2):
    """Return number of days between two datetime objects"""
    return (date2 - date1).days

def add_days(date, n):
    """Return date + n days"""
    return date + timedelta(days=n)
