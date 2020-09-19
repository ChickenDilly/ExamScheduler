import School
import Calendar
import setup


def main():
    menu = "Select a menu option. " \
           "\n 0. Quit \n 1. Create calendar entries. \n 2. View calendar entries."
    selection = ""

    while selection != "0":
        setup.setup()
        selection = input(menu)

        if selection == "1":
            all_classes = list()
            class_name = input("Enter the class name or press (Q) to quit. \n")

            while class_name.upper() != "Q":
                all_classes.append(School.SchoolClass.new_school_class(class_name))
                class_name = input("Enter the class name or press (Q) to quit.\n")

            try:
                if all_classes[0].all_exams:
                    calendar_id = Calendar.new_calendar()
                    for school_class in all_classes:
                        # creates a new event for each exam date
                        Calendar.set_events(school_class, calendar_id)

                elif not all_classes[0].all_exams:
                    print("No exams to enter. \n")

            except IndexError:
                print("No classes were entered.\n")

        elif selection == "2":
            events = int(input("How many events to list?"))
            Calendar.view_events(events, Calendar.return_calendar_id())


if __name__ == '__main__':
    main()
