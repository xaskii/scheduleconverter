# Timetable to .ICS tool

Converts "Detailed Schedule" page from Carleton Central to an **icalendar** file that you can import a calendar app of your choice

## Usage

```bash
uv sync
uv run scheduleexporter/converter.py \<path of paste here\>
```

## TODO

- [ ] Add e2e tests comparing generated `.ics` files
- [ ] Switch back over to requirements.txt
- [ ] Turn into small web-app and deploy it on a box somewhere

## Notes

- Timezones are really scary 😟
