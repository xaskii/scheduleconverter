import re
from datetime import timedelta
from pprint import pprint


def objprint(obj):
    pprint(obj.__dict__, indent=2)


def i_cal_to_string(cal):
    return cal.to_ical().decode("utf-8").replace("\r\n", "\n").strip()


def on_day(dt, day):
    return dt + timedelta(days=(day - dt.weekday()) % 7)


def get_next_weekday(dt, dayChar):
    lookup = {
        "M": 0,
        "T": 1,
        "W": 2,
        "R": 3,
        "F": 4,
    }
    return on_day(dt, lookup[dayChar])


def days_to_rrule(days):
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


def onDay(dt, day):
    return dt + timedelta(days=(day - dt.weekday()) % 7)


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


def parse_line(line):
    for (
        key,
        rx,
    ) in REGEX_DICTIONARY.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None


WEEKDAYS = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}
