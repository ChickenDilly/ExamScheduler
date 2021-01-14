import re
import datetime


class CollegeClass:
    def __init__(self, class_name):
        self.class_name = class_name
        self.all_exams = dict()

    @staticmethod
    # upon creation of a new class, all possible exams. hw, etc is added to a dict in the object
    def new_school_class(newClass):
        MM_DD_pattern = re.compile(r'\d\d+-\d\d+')     # mm-dd format, includes out of bounds dates
        #YY_MM_DD_pattern = re.compile(r'\d\d+-\d\d+-\d\d')
        temp_class = CollegeClass(newClass)
        input_data = str(input("Enter an exam name and date (mm-dd) or press (Q) to quit."))

        while input_data.upper() != 'Q':
            # checks for valid pattern inputs
            if MM_DD_pattern.search(input_data) is not None:
                exam_date = MM_DD_pattern.search(input_data).group(0)
                exam_date_month = int(exam_date[:exam_date.find('-')])
                exam_date_day = int(exam_date[exam_date.find('-') + 1:])

                # exam name is everything before the exam day
                if input_data[:input_data.find(exam_date)] is not '':
                    exam_name = input_data[:input_data.find(exam_date) - 1]

                    # error checking for correct date format
                    try:
                        exam_date = datetime.datetime(day=exam_date_day, month=exam_date_month,
                                                      year=datetime.datetime.today().year)
                        temp_class.all_exams['{}'.format(exam_name)] = exam_date.strftime('%m-%d')
                    except ValueError:
                        print("Invalid date entered. Try again.")

            else:
                print("Patterns not found. Try again. \n")

            input_data = str(input("Enter an exam name and date (mm-dd) or press (Q) to quit."))

        return temp_class
