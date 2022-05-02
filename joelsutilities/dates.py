from datetime import datetime, timedelta, tzinfo
from typing import Optional, Union

import pytz
from pytz.tzinfo import DstTzInfo, StaticTzInfo

from .exceptions import DateTimeException


def format_timedelta(td: timedelta, fmt: str = "{h:02}:{m:02}:{s:02}") -> str:
    """format timedelta object with format spec
    
    valid format specifiers include:
    
    - d: days
    - h: hours
    - m: minutes
    - s: seconds
    - ms: milliseconds
    - u: microseconds
    

    :param timedelta td: ``timdelta`` object
    :param str fmt: string formatter, defaults to "{h:02}:{m:02}:{s:02}"
    :return str: ``timdelta`` object formatted as a strning
    

    >>> format_timedelta(timedelta(seconds=30, minutes=20))
    "00:30:20"
    >>> format_timedelta(timedelta(days=2, hours=3), '{d} days')
    "2 days"
    >>> format_timedelta(timedelta(days=2, hours=3, minutes=4, seconds=5, milliseconds=6), '{d} days {h:02}:{m:02}:{s:02}:{ms:03}')
    "2 days 03:04:05:006"
    """    
    s = td.total_seconds()
    formatters = {
        "u": td.microseconds,
        "ms": int(td.microseconds / 1000),
        "s": int(s) % 60,
        "m": int(s / 60) % 60,
        "h": int(s / (60 * 60)) % 24,
        "d": td.days,
    }
    return fmt.format(**formatters)


def localise(dt: datetime, tz_from: Union[DstTzInfo, StaticTzInfo] = pytz.UTC, tz_to=pytz.timezone("Europe/London")) -> datetime:     
    """convert naive datetime (default UTC) into local datetime (default London)

    :param datetime.datetime dt: datetime input
    :param typing.Union[DstTzInfo, StaticTzInfo] tz_from: timezone to convert from, defaults to pytz.UTC
    :param _type_ tz_to: timzone to convert to, defaults to pytz.timezone("Europe/London")
    :raises DateTimeException: expects datetime to be naive
    :return datetime: timezone aware datetime
    """    
    if dt.tzinfo:
        raise DateTimeException("expected datetime to be naive")
    return tz_from.localize(dt).astimezone(tz_to)


def today(tz: Optional[tzinfo]=None) -> datetime:
    """get datetime of today"""
    now = datetime.now(tz)
    return datetime(year=now.year, month=now.month, day=now.day)


def tomorrow(tz: Optional[tzinfo]=None) -> datetime:
    """get datetime of tomorrow"""
    return today(tz) + timedelta(days=1)
