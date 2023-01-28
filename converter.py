import re
import os
import pytz
from icalendar import Calendar, Event,  vDDDTypes
from datetime import datetime, timedelta
from dateutil.parser import parse

from helper import objprint, i_cal_to_string, get_next_weekday, days_to_rrule


class Course:
    def __init__(self, name, code, section):
        self.name = name
        self.code = code
        self.section = section


courseList = []

rx_dict = {
    'course': re.compile(r'(?P<name>.+) - (?P<code>.+) - (?P<section>\w+)\n'),
    'instructor': re.compile(r'Assigned Instructor:\s(?P<instructor>.+)\n'),
    'classInfo': re.compile(r'Class\t(?P<startTime>\d{1,2}:\d{2} \w{2}) - (?P<endTime>\d{1,2}:\d{2} \w{2})\t('
                            r'?P<days>\w+)\t(?P<building>.*)\t(?P<startDate>.*)\ - (?P<endDate>.*)\t(?P<type>.*)\t.*\n')
}

timezone = pytz.timezone("US/Eastern")

weekdays = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6,
}


def onDay(dt, day):
    return dt + timedelta(days=(day-dt.weekday()) % 7)


def _parse_line(line):
    for key, rx, in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None


def parse_file(path):
    data = []
    with open(path, 'r') as file:
        for line in file:
            key, match = _parse_line(line)

            if key == 'course':
                new_course = None
                name = match.group('name')
                code = match.group('code')
                section = match.group('section')
                new_course = Course(name, code, section)

            if key == 'instructor':
                new_course.instructor = match.group('instructor')

            if key == 'classInfo':
                new_course.location = match.group('building')
                # TODO: parse into date objects? done haha
                new_course.type = match.group('type')
                new_course.times = {
                    'start': parse(match.group('startTime')),
                    'end': parse(match.group('endTime'))
                }
                new_course.dates = {
                    'start': parse(match.group('startDate')),
                    'end': parse(match.group('endDate'))
                }
                # TODO: figure out starting days
                new_course.days = match.group('days')
                courseList.append(new_course)

    pass


parse_file('paste.test.txt')
# parse_file('course.test.txt')


cal = Calendar()
rruleTemplate = []

for course in courseList:
    event = Event()
    event['summary'] = f'{course.code}-{course.section}'
    event['description'] = course.name
    event['location'] = course.location

    # untilDate = vDDDTypes(course.dates['end']).to_ical().decode('utf-8')
    untilDate = course.dates['end']
    startDate = vDDDTypes(datetime.combine(
        get_next_weekday(course.dates['start'].date(), course.days[0]), course.times['start'].time()))

    event['dtstart'] = startDate
    event['duration'] = vDDDTypes(course.times['end'] - course.times['start'])
    # event['rrule'] = [
    #     'FREQ=WEEKLY',
    #     'COUNT=12',
    #     f'UNTIL={untilDate}',
    #     # ESCAPES THE COMMAS???? WHAT DO I DO LOL???
    #     # ?????????????????????????????????????
    #     f'BYDAY={days_to_rrule(course.days)}'
    # ]
    # FOUND FORMAT IN GITHUB ISSUE
    event.add('rrule', {
        'FREQ': 'WEEKLY',
        'COUNT': 12,
        'UNTIL': untilDate,
        'BYDAY': days_to_rrule(course.days)
    })

    cal.add_component(event)

    # break  # making first event

# print(i_cal_to_string(cal))

# write to file
directory = os.getcwd()
f = open(os.path.join(directory, 'example.ics'), 'wb')
f.write(cal.to_ical())
f.close()


print("CALENDAR SUMMARY:\n")
e = open('example.ics', 'rb')
ecal = Calendar.from_ical(e.read())
for component in ecal.walk():
    if component.name == "VEVENT":
        print(component.get("summary"))
        print(component.get("description"))
        print(component.get("organizer"))
        print(component.get("location"))
        print(component.decoded("dtstart"))
        print(component.decoded("duration"))
        print()
e.close()
