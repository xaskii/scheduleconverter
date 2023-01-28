from pprint import pprint
from datetime import datetime, timedelta


def objprint(obj):
    pprint(obj.__dict__, indent=2)


def i_cal_to_string(cal):
    return cal.to_ical().decode("utf-8").replace('\r\n', '\n').strip()


def on_day(dt, day):
    return dt + timedelta(days=(day-dt.weekday()) % 7)


def get_next_weekday(dt, dayChar):
    lookup = {
        'M': 0,
        'T': 1,
        'W': 2,
        'R': 3,
        'F': 4,
    }
    return on_day(dt, lookup[dayChar])


def days_to_rrule(days):
    codes = []
    lookup = {
        'M': 'MO',
        'T': 'TU',
        'W': 'WE',
        'R': 'TH',
        'F': 'FR',
    }
    for day in days:
        codes.append(lookup[day])

    return codes
