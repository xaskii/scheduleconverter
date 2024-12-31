# Timetable to .ICS tool

Converts "Detailed Schedule" page from Carleton Central to an **icalendar** file that you can import a calendar app of your choice

## Usage

```bash
# If you have uv installed already
uv run schedule-exporter --help
uv run schedule-exporter paste.txt
```

```bash
# Creating virtual env and installing dependencies
python -m venv .venv
source ./.venv/bin/activate
pip install -r pyproject.toml

# Using the tool
schedule-exporter --help
schedule-exporter paste.txt
```

## TODO

- [ ] get rid of 'icalendar' dependency, and create an ICS file based on the RFC (in source control)
- [ ] Add e2e tests comparing generated `.ics` files
- [ ]
