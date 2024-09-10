import os
from argparse import ArgumentParser
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from dateutil.parser import parse
from icalendar import Calendar, Event, vDDDTypes

from scheduleexporter.helper import days_to_rrule, get_next_weekday, parse_line

DEFAULT_OUTPUT_FILE = "timetable.ics"
CALENDAR_SUMMARY_FILE = "example.ics"


@dataclass
class Course:
    name: str
    code: str
    section: str
    instructor: str = ""
    location: str = ""
    _type: str = ""
    times: Dict[str, datetime] = field(default_factory=dict)
    dates: Dict[str, datetime] = field(default_factory=dict)
    days: str = ""


@dataclass
class CalendarEvent:
    summary: str
    description: str
    location: str
    start_time: datetime
    duration: timedelta
    end_date: datetime
    days: str


def ingest_paste(filepath: Path) -> List[Course]:
    course_list: List[Course] = []
    try:
        with filepath.open("r") as file:
            current: Optional[Course] = None
            for line in file:
                key, match = parse_line(line)
                if not match:
                    continue

                if key == "course":
                    name = match.group("name")
                    code = match.group("code")
                    section = match.group("section")
                    current = Course(name, code, section)

                elif key == "instructor" and current:
                    current.instructor = match.group("instructor")

                elif key == "classInfo" and current:
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

    except IOError as e:
        print(f"Error reading file: {e}")
        raise

    return course_list


def create_calendar_event(course: Course) -> CalendarEvent:
    first_day = min(
        (get_next_weekday(course.dates["start"].date(), day) for day in course.days)
    )
    start_time = datetime.combine(first_day, course.times["start"].time())
    duration = course.times["end"] - course.times["start"]
    end_date = course.dates["end"]

    return CalendarEvent(
        summary=f"{course.code}-{course.section}",
        description=course.name,
        location=course.location,
        start_time=start_time,
        duration=duration,
        end_date=end_date,
        days=course.days,
    )


def create_ical_event(calendar_event: CalendarEvent) -> Event:
    event = Event()
    event["summary"] = calendar_event.summary
    event["description"] = calendar_event.description
    event["location"] = calendar_event.location
    event["dtstart"] = vDDDTypes(calendar_event.start_time)
    event["duration"] = vDDDTypes(calendar_event.duration)
    event.add(
        "rrule",
        {
            "FREQ": "WEEKLY",
            "UNTIL": calendar_event.end_date + timedelta(days=1),
            "BYDAY": days_to_rrule(calendar_event.days),
        },
    )
    return event


def write_calendar(cal: Calendar, filepath: str):
    with open(filepath, "wb") as f:
        f.write(cal.to_ical())


def print_calendar_summary(filepath: str):
    print("CALENDAR SUMMARY:\n")
    with open(filepath, "rb") as f:
        ecal = Calendar.from_ical(f.read().decode("utf-8"))
        for component in ecal.walk():
            if component.name == "VEVENT":
                print(f"Summary: {component.get('summary')}")
                print(f"Description: {component.get('description')}")
                print(f"Location: {component.get('location')}")
                print(f"Start time: {component.decoded('dtstart')}")
                print(f"Duration: {component.decoded('duration')}")
                print()


def main():
    parser = ArgumentParser(
        description="Converts schedule paste into an icalendar file for import into the calendar application of your choice"
    )
    parser.add_argument("input", help="Path to paste containing default schedule")
    parser.add_argument(
        "-o",
        "--output_file",
        default=DEFAULT_OUTPUT_FILE,
        help="Output file path",
    )
    args = parser.parse_args()

    calendar_path = Path(args.input)

    if not calendar_path.exists():
        print("Filepath not found, please check the path you've given.")
        return 1

    try:
        course_list = ingest_paste(calendar_path)
    except Exception as e:
        print(f"Error ingesting paste: {e}")
        return 1

    cal = Calendar()

    for course in course_list:
        cal_event = create_calendar_event(course)
        ical_event = create_ical_event(cal_event)
        cal.add_component(ical_event)

    output_path = os.path.join(os.getcwd(), CALENDAR_SUMMARY_FILE)
    write_calendar(cal, output_path)
    print_calendar_summary(output_path)

    return 0


if __name__ == "__main__":
    exit(main())
