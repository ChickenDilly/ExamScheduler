import src.Calendar
import src.main
import src.School
from datetime import datetime, timedelta


def main():
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    exams = {
            'exam 1': '{}-{}'.format(today.month, today.day),
            'exam 2': '{}-{}'.format(tomorrow.month, tomorrow.day)
    }

    class_1 = src.School.SchoolClass('Class 1')
    class_2 = src.School.SchoolClass('Class 2')
    class_1.list_of_exams = exams
    class_2.list_of_exams = exams

    classes = list()
    classes.append(class_1)
    classes.append(class_2)

    calendar_id = src.Calendar.new_calendar()
    for example_class in classes:
        src.Calendar.set_events(example_class, calendar_id)

    src.Calendar.view_events(10, calendar_id)


if __name__ == "__main__":
    main()

