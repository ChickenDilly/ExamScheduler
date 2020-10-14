import re


class SchoolClass:
    def __init__(self, class_name):
        self.class_name = class_name
        self.all_exams = dict()

    @staticmethod
    # upon creation of a new class, all possible exams. hw, etc is added to a dict in the object
    def new_school_class(school_class):
        exam_pattern = re.compile(r'^\D+\s\w+')     # finds first 2 words
        day_pattern = re.compile('\\d\\d+-\\d\\d+')     # mm-dd format, includes out of bounds dates

        temp_class = SchoolClass(school_class)
        input_data = str(input("Enter an exam name and date (mm-dd) or press (Q) to quit."))

        while input_data.upper() != 'Q':
            # checks for valid pattern inputs
            if (exam_pattern.search(input_data) is not None) and (day_pattern.search(input_data) is not None):
                exam_date = day_pattern.search(input_data).group(0)
                exam_name = input_data[:input_data.find(exam_date)]

                # error checking for correct date format
                if int(exam_date[0:2]) <= 12 or int(exam_date[3:5]) <= 31:
                    temp_class.all_exams['{}'.format(exam_name)] = exam_date
                else:
                    print("Invalid date entered. Try again.")

            else:
                print("Patterns not found. Try again. \n")

            input_data = str(input("Enter an exam name and date (mm-dd) or press (Q) to quit."))

        return temp_class
