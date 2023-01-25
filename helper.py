from pprint import pprint
from datetime import datetime, timedelta


def objprint(obj):
    pprint(obj.__dict__, indent=2)


def iCalToString(cal):
    return cal.to_ical().decode("utf-8").replace('\r\n', '\n').strip()


def onDay(dt, day):
    return dt + timedelta(days=(day-dt.weekday()) % 7)


def getNextWeekday(dt, dayChar):
    lookup = {
        'M': 0,
        'T': 1,
        'W': 2,
        'R': 3,
        'F': 4,
    }
    return onDay(dt, lookup[dayChar])


def daysToRRULE(days):
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
