import os
from argparse import ArgumentParser
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from dateutil.parser import parse
from icalendar import Calendar, Event, vDDDTypes

from scheduleexporter.helper import days_to_rrule, get_next_weekday, parse_line


@dataclass
class Course:
    name: str
    code: str
    section: str
    instructor: str = ""
    location: str = ""
    _type: str = ""
    times: dict[str, datetime] = field(default_factory=dict)
    dates: dict[str, datetime] = field(default_factory=dict)
    days: str = ""


def ingest_paste(filepath: Path) -> list[Course]:
    course_list = []
    with filepath.open("r") as file:
        current = None
        for line in file:
            key, match = parse_line(line)
            if not match:
                continue

            if key == "course":
                name = match.group("name")
                code = match.group("code")
                section = match.group("section")
                current = Course(name, code, section)

            if key == "instructor":
                assert type(current) is Course
                current.instructor = match.group("instructor")

            if key == "classInfo":
                assert type(current) is Course
                current.location = match.group("building")
                current._type = match.group("type")
                current.times = {
                    "start": parse(match.group("startTime")),
                    "end": parse(match.group("endTime")),
                }
                current.dates = {
                    "start": parse(match.group("startDate")),
                    "end": parse(match.group("endDate")),
                }
                current.days = match.group("days")
                course_list.append(current)
                current = None

    return course_list


def main():
    parser = ArgumentParser(
        description="""Converts schedule paste into an icalendar file for import into the calendar application of your choice"""
    )
    parser.add_argument("input_file", help="Path to paste containing default schedule")
    parser.add_argument(
        "-o",
        "--output_file",
        default="timetable.ics",
        required=False,
        help="Output file path",
    )
    args = parser.parse_args()

    calendar_path = Path(args.path)

    if not calendar_path.exists():
        print("Filepath not found, please check the path you've given.")
        raise SystemExit(1)

    course_list = ingest_paste(calendar_path)
    # parse_file('course.test.txt')

    cal = Calendar()

    for course in course_list:
        event = Event()
        event["summary"] = f"{course.code}-{course.section}"
        event["description"] = course.name
        event["location"] = course.location

        # untilDate = vDDDTypes(course.dates['end']).to_ical().decode('utf-8')
        untilDate = course.dates["end"]
        startDate = vDDDTypes(
            datetime.combine(
                get_next_weekday(course.dates["start"].date(), course.days[0]),
                course.times["start"].time(),
            )
        )

        event["dtstart"] = startDate
        event["duration"] = vDDDTypes(course.times["end"] - course.times["start"])
        event.add(
            "rrule",
            {
                "FREQ": "WEEKLY",
                "COUNT": 12,
                "UNTIL": untilDate,
                "BYDAY": days_to_rrule(course.days),
            },
        )
        cal.add_component(event)

    # write to file
    f = open(os.path.join(os.getcwd(), "example.ics"), "wb")
    f.write(cal.to_ical())
    f.close()

    print("CALENDAR SUMMARY:\n")
    e = open("example.ics", "rb")
    ecal = Calendar.from_ical(e.read().decode("utf-8"))
    for component in ecal.walk():
        if component.name == "VEVENT":
            print(component.get("summary"))
            print(component.get("description"))
            print(component.get("location"))
            print(component.decoded("dtstart"))
            print(component.decoded("duration"))
            print()
    e.close()

if __name__ == "__main__":
    main()
