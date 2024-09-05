import re
from datetime import date, timedelta
from pprint import pprint
from typing import Optional

from icalendar import Calendar

REGEX_DICTIONARY = {
    "course": re.compile(r"(?P<name>.+) - (?P<code>.+) - (?P<section>\w+)\n"),
    "instructor": re.compile(r"Assigned Instructor:\s(?P<instructor>.+)\n"),
    "classInfo": re.compile(
        r"Class\t(?P<startTime>\d{1,2}:\d{2} \w{2}) - "
        r"(?P<endTime>\d{1,2}:\d{2} \w{2})\t("
        r"?P<days>\w+)\t(?P<building>.*)\t(?P<startDate>.*) - "
        r"(?P<endDate>.*)\t(?P<type>.*)\t.*\n"
    ),
}


def objprint(obj):
    pprint(obj.__dict__, indent=2)


def ical_to_string(cal: Calendar) -> str:
    return cal.to_ical().decode("utf-8").replace("\r\n", "\n").strip()


def on_day(dt: date, day: int):
    return dt + timedelta(days=(day - dt.weekday()) % 7)


def get_next_weekday(dt: date, dayChar: str):
    lookup = {
        "M": 0,
        "T": 1,
        "W": 2,
        "R": 3,
        "F": 4,
    }
    return on_day(dt, lookup[dayChar])


def days_to_rrule(days: str) -> list[str]:
    codes = []
    lookup = {
        "M": "MO",
        "T": "TU",
        "W": "WE",
        "R": "TH",
        "F": "FR",
    }
    for day in days:
        codes.append(lookup[day])

    return codes


def parse_line(line: str) -> tuple[Optional[str], Optional[re.Match]]:
    for key, pattern in REGEX_DICTIONARY.items():
        if match := pattern.search(line):
            return key, match
    return None, None
