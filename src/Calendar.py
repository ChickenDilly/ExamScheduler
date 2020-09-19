from setup import setup
import School
from datetime import datetime, timedelta


def get_calendar_service():
    return setup()


def new_calendar():
    service = get_calendar_service()
    calendar_format = {'summary': 'Exam Schedule', 'timeZone': 'America/New_York'}
    selection = str(input("Press (U) to update the calendar or (D) to delete old entries."))
    page_token = None

    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:

            if calendar_list_entry['summary'] == 'Exam Schedule':
                if selection.upper() == "D":
                    service.calendars().delete(calendarId=calendar_list_entry['id']).execute()
                    break
                elif selection.upper() == "U":
                    return calendar_list_entry['id']
                else:
                    print("Invalid entry. Try again.")
                    new_calendar()

        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    calendar = service.calendars().insert(body=calendar_format).execute()
    return calendar['id']


def return_calendar_id():
    service = get_calendar_service()
    calendar_format = {'summary': 'Exam Schedule', 'timeZone': 'America/New_York'}
    page_token = None

    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == 'Exam Schedule':

                return calendar_list_entry['id']

        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    calendar = service.calendars().insert(body=calendar_format).execute()
    return calendar['id']


def set_events(school_class: School.SchoolClass, exam_calendar_id: str):
    service = get_calendar_service()
    exam_list = school_class.all_exams
    today = datetime.today()

    for key in exam_list:
        # yyyy-mm-dd format
        temp_string = "{0}-{1}".format(today.year, exam_list[key])
        exam_date = datetime.strptime(temp_string, "%Y-%m-%d").date()
        summary = "{0} {1} {2}".format(school_class.class_name, key, exam_list[key])
        timezone = "America/New_York"

        if "quiz" in key.lower() or "homework" in key.lower():
            # event starts 10 days prior to quiz
            start_time = "{}T10:00:00.000".format(exam_date - timedelta(days=10))
            end_time = "{}T12:00:00.000".format(exam_date - timedelta(days=10))
            recurrence_rule = "RRULE:FREQ=DAILY;INTERVAL=2;COUNT=6"

        else:
            # event starts 2 weeks prior to the exam
            start_time = "{}T10:00:00.000".format(exam_date - timedelta(days=15))
            end_time = "{}T12:00:00.000".format(exam_date - timedelta(days=15))
            recurrence_rule = "RRULE:FREQ=DAILY;INTERVAL=3;COUNT=6"

        # new alert every X days (3 for exams, 2 for quizzes)
        event_format = {
            "summary": summary,
            "start": {
                "dateTime": start_time,
                "timeZone": timezone
            },
            "end": {
                "dateTime": end_time,
                "timeZone": timezone
            },
            "recurrence": [recurrence_rule],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {'method': 'email', 'minutes': 10}
                ]
            }
        }

        service.events().insert(calendarId=exam_calendar_id, body=event_format).execute()


def view_events(items: int, calendar_id):
    service = get_calendar_service()
    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting List {} events'.format(items))
    events_result = service.events().list(
       calendarId=calendar_id, timeMin=now,
       maxResults=items, singleEvents=True,
       orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    for event in events:
        start = event['start'].get("dateTime")
        index = start.find('T')
        just_time = start[:index]

        print(just_time, event['summary'])
