from src.setup import setup
import src.School as School
from datetime import datetime, timedelta
import re


def get_calendar_service():
    # needed for calendar authorization
    return setup()


def new_calendar():
    # adds all events to the exam schedule calendar, or new calendar if it doesn't exist
    service = get_calendar_service()
    calendar_format = {"summary": "Exam Schedule", "timeZone": "America/New_York"}
    selection = str(
        input("Press (U) to update the calendar or (D) to delete old entries.")
    )
    page_token = None

    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list["items"]:

            if calendar_list_entry["summary"] == "Exam Schedule":
                if selection.upper() == "D":
                    if (
                        input(
                            "Are you sure you want to delete old events? (y/n)"
                        ).upper()
                        == "Y"
                    ):
                        service.calendars().delete(
                            calendarId=calendar_list_entry["id"]
                        ).execute()
                        break
                    else:
                        print("Invalid entry. Try again.")
                        new_calendar()
                elif selection.upper() == "U":
                    return calendar_list_entry["id"]
                else:
                    print("Invalid entry. Try again.")
                    new_calendar()

        page_token = calendar_list.get("nextPageToken")
        if not page_token:
            break

    calendar = service.calendars().insert(body=calendar_format).execute()
    return calendar["id"]


def return_calendar_id():
    # creates an exam schedule calendar, if it doesn't exist, and returns the exam schedule calendar id
    service = get_calendar_service()
    calendar_format = {"summary": "Exam Schedule", "timeZone": "America/New_York"}
    page_token = None

    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list["items"]:
            if calendar_list_entry["summary"] == "Exam Schedule":

                return calendar_list_entry["id"]

        page_token = calendar_list.get("nextPageToken")
        if not page_token:
            break

    calendar = service.calendars().insert(body=calendar_format).execute()
    return calendar["id"]


def set_events(school_class: School.CollegeClass, exam_calendar_id: str):
    service = get_calendar_service()
    exam_list, remaining_keys = school_class.all_exams, list(
        school_class.all_exams.keys()
    )
    today = datetime.today()
    all_summaries = get_events_summaries(exam_calendar_id)

    # sets all events from a class to the calendar
    for key in exam_list:
        # yyyy-mm-dd format
        temp_string = "{0}-{1}".format(today.year, exam_list[key])
        exam_date = datetime.strptime(temp_string, "%Y-%m-%d").date()
        summary = "{0} {1} {2}".format(school_class.class_name, key, exam_list[key])
        timezone = "America/New_York"
        remaining_keys.remove(key)

        if "quiz" or "homework" or "hw" or "lab" in key.lower():
            # event starts 10 days prior to quiz
            start_time = "{}T10:00:00.000".format(exam_date - timedelta(days=10))
            end_time = "{}T12:00:00.000".format(exam_date - timedelta(days=10))
            recurrence_rule = "RRULE:FREQ=DAILY;INTERVAL=2;COUNT=6"

        else:
            # event starts 2 weeks prior to the exam
            start_time = "{}T10:00:00.000".format(exam_date - timedelta(days=15))
            end_time = "{}T12:00:00.000".format(exam_date - timedelta(days=15))
            recurrence_rule = "RRULE:FREQ=DAILY;INTERVAL=3;COUNT=6"

        # new alert every X days (3 for exams, 2 for quizzes/hw)
        event_format = {
            "summary": summary,
            "start": {"dateTime": start_time, "timeZone": timezone},
            "end": {"dateTime": end_time, "timeZone": timezone},
            "recurrence": [recurrence_rule],
            "reminders": {
                "useDefault": False,
                "overrides": [{"method": "email", "minutes": 10}],
            },
        }

        # identical summaries won't be added again
        if key in remaining_keys:
            continue
        if summary in all_summaries:
            continue
        else:
            service.events().insert(
                calendarId=exam_calendar_id, body=event_format
            ).execute()


def get_events_summaries(calendar_id):
    service = get_calendar_service()
    events_result = (
        service.events()
        .list(calendarId=calendar_id, singleEvents=True, orderBy="startTime")
        .execute()
    )
    all_events = events_result.get("items", [])

    index = 0
    for event in all_events:
        all_events[index] = event["summary"]
        index += 1

    return list(set(all_events))


def view_events(items: int, calendar_id):
    # prints the next X events from today's date
    # not able to return all events
    now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time

    service = get_calendar_service()
    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=items,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return

    for event in events:
        start = event["start"].get("dateTime")
        index = event["start"].get("dateTime").find("T")
        just_time = start[:index]

        print(just_time, event["summary"])


def weekly_events(calendar_id, _week, search_class):
    # finds and prints the due dates for the next X days with no duplicates.
    service = get_calendar_service()
    service_results = (
        service.events()
        .list(
            calendarId=calendar_id,
            singleEvents=True,
            orderBy="startTime",
            maxResults=1000,
        )
        .execute()
    )
    __events = service_results.get("items", [])

    # there's nothing to check validity of input class to list of classes
    # checks if class search is enabled
    enable_class_search = search_class != ""

    # format: mm-dd
    date_pattern = re.compile(r"[0-1][0-9]-[0-3][0-9]")
    week = _week  # number of days defined as a week
    weeks_events = list()
    today = datetime.today()
    last_event_day = today + timedelta(days=week + 1)
    event_index = 0

    # from all events in the calendar ...
    # all duplicates wont be added to weeks_events
    for event in __events:
        event_index = event_index + 1
        calendar_start_date = event["start"]["dateTime"]
        if (
            datetime.strptime(calendar_start_date, "%Y-%m-%dT%H:%M:%S%z").date()
            == last_event_day.date()
        ):
            break

        # when class search's enabled, only events containing search_class
        if enable_class_search:
            if event["summary"].find(search_class) != -1:
                pass
            else:
                continue

        event_date = date_pattern.search(event["summary"]).group(0)
        event_month, event_day = int(event_date[0:2]), int(event_date[3:])

        # looks for the events in the next X days, checking all calendar events
        try:
            event_datetime = datetime(month=event_month, day=event_day, year=today.year)

            if (
                timedelta(days=week)
                >= event_datetime - today.replace(hour=0, minute=0, second=0)
                >= timedelta(days=0)
            ):
                equal_summary = False

                for index_weeks in range(0, len(weeks_events), 1):
                    summary_tested = event["summary"]

                    # if duplicate exists, stop checking
                    if len(weeks_events) > 0:
                        if summary_tested == weeks_events[index_weeks]["summary"]:
                            equal_summary = True
                            break

                # no duplicates, item added
                if not equal_summary:
                    weeks_events.append(event)

        # confirms events must have event dates
        except AttributeError:
            continue

    if len(weeks_events) == 0:
        print("No events are upcoming in the next {} days.".format(week))

    else:
        print(r"Getting this week's events...")
        for event in weeks_events:
            print(event["summary"])
