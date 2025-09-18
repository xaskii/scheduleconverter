import re
from datetime import date, timedelta
from enum import Enum
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


class Weekday(Enum):
    M = (0, "MO")
    T = (1, "TU")
    W = (2, "WE")
    R = (3, "TH")
    F = (4, "FR")

    @property
    def weekday_index(self) -> int:
        return self.value[0]

    @property
    def rrule_code(self) -> str:
        return self.value[1]


def get_next_weekday(dt: date, day_char: str) -> date:
    target_weekday = Weekday[day_char]
    return dt + timedelta(days=(target_weekday.weekday_index - dt.weekday()) % 7)


def days_to_rrule(days: str) -> list[str]:
    return [Weekday[day].rrule_code for day in days]


def parse_line(line: str) -> tuple[Optional[str], Optional[re.Match]]:
    for key, pattern in REGEX_DICTIONARY.items():
        if match := pattern.search(line):
            return key, match
    return None, None


def objprint(obj):
    pprint(obj.__dict__, indent=2)


def ical_to_string(cal: Calendar) -> str:
    return cal.to_ical().decode("utf-8").replace("\r\n", "\n").strip()
