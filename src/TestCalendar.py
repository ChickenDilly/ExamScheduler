import Calendar
import main
from datetime import datetime, timedelta


def main():
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    exams = {
            'exam 1': '{}-{}'.format(today.month, today.day),
            'exam 2': '{}-{}'.format(tomorrow.month, tomorrow.day)
    }

    class_1 = main.SchoolClass('Class 1')
    class_2 = main.SchoolClass('Class 2')
    class_1.list_of_exams = exams
    class_2.list_of_exams = exams

    classes = list()
    classes.append(class_1)
    classes.append(class_2)

    calendar_id = Calendar.new_calendar()
    for example_class in classes:
        Calendar.set_events(example_class, calendar_id)

    Calendar.view_events(10, calendar_id)


if __name__ == "__main__":
    main()

