import re
import icalendar
from pprint import pprint


class Course:
    def __init__(self, info):
        self.name = info.name
        self.code = info.code
        self.section = info.section

courseList = []

rx_dict = {
    'course': re.compile(r'(?P<name>.+) - (?P<code>.+) - (?P<section>\w+)\n'),
    'instructor': re.compile(r'Assigned Instructor:\s(?P<instructor>.+)\n'),
    'classInfo': re.compile(r'Class\t(?P<startTime>\d:\d{2} \w{2}) - (?P<endTime>\d:\d{2} \w{2})\t(?P<days>\w+)\t(?P<building>.*)\t(?P<startDate>.*)\ - (?P<endDate>.*)\t(?P<type>.*)\t.*\n')
}


def _parse_line(line):
    for key, rx, in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None


def parse_file(path):
    data = []
    with open(path, 'r') as file:
        line = file.readline()
        while line:
            key, match = _parse_line(line)

            if key == 'course':
                name = match.group('name')
                code = match.group('code')
                section = match.group('section')
                print(name, code, section)

            if key == 'instructor':
                pass

            if key == 'classInfo':
                pass

            line = file.readline()

    return data

parse_file('course.txt')

for course in courseList:
    pprint(course.__dict__, indent=2)
