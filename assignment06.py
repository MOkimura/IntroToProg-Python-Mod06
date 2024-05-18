# ------------------------------------------------------------------------------------------ #
# Title: assignment06
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: Michael Okimura, 05/17/2024, Created Script
# ------------------------------------------------------------------------------------------ #
import json
from sys import exit

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
# Define the Data Constants
FILE_NAME: str = "enrollments.json"

# Define the Data Variables and constants
student_first_name: str = ''  # Holds the first name of a student entered by the user.
student_last_name: str = ''  # Holds the last name of a student entered by the user.
course_name: str = ''  # Holds the name of a course entered by the user.
student_data: dict = {}  # one row of student data
students: list = []  # a table of student data
csv_data: str = ''  # Holds combined string data separated by a comma.
json_data: str = ''  # Holds combined string data in a json format.
file = None  # Holds a reference to an opened file.
menu_choice: str  # Hold the choice made by the user.
choice: str # Input variable for selecting the menu option.

# This class will handle the reading and writing of the json file.
class FileProcessor:

    # Function for reading the enrollments.json file at program open. Error message will display if file does not already exist.
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        try:
            with open(file_name, "r") as file:
                student_data = json.load(file)
        except FileNotFoundError as error_message:
            IO.output_error_messages("File for enrollments does not exist.", error_message)
        return student_data

    # Function for writing to the enrollments.json file upon menu selection. Error handling for no pre-existing file but it won't trigger because it's opening in write mode.
    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        try:
            with open(file_name, "w") as file:
                json.dump(student_data, file)
        except FileNotFoundError as error_message:
            IO.output_error_messages("File for enrollments does not exist.", error_message)

# This class will save and display data from the inputs, json file, and error messages.
class IO:

    # Displays the type of error that occurs with additional details.
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        print(message, end="\n\n")
        if error is not None:
            print("-- Exception details --")
            print(error, error.__doc__, type(error), sep="\n")
    
    # Displays the menu of options.
    @staticmethod
    def output_menu(menu: str):
        print(MENU, end="\n\n")

    # Input for the menu option. Will display error if an invalid option is selected until a valid option is selected.
    @staticmethod
    def input_menu_choice():
        choice = "0"
        try:
            choice = input("What would you like to do: ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("You must choose: 1, 2, 3, or 4")
        except Exception as error_message:
            IO.output_error_messages(error_message.__str__())
        return choice

    # Displays the current data.
    @staticmethod
    def output_student_courses(student_data: list):
        print("-"*40)
        for item in student_data:
            print(f"{item["FirstName"]} {item["LastName"]} is enrolled in {item["CourseName"]}")
        print("-"*40, end="\n\n")

    # Inputs for the first, last, and course name. Error will display is no data is entered until data is entered.
    @staticmethod
    def input_student_data(student_data: list):
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name:
                raise ValueError("Cannot enter blank information.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name:
                raise ValueError("Cannot enter blank information.")
            course_name = input("Enter the course name: ")
            if not course_name:
                raise ValueError("Cannot enter blank information.")
            student_data.append({"FirstName": student_first_name, "LastName": student_last_name, "CourseName": course_name})
        except ValueError as error_message:
            IO.output_error_messages("Cannot enter blank information.", error_message)
        return student_data

# Start of program
if __name__ == "__main__":
    students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

    # Displays menu of options
    while True:
        IO.output_menu(MENU)
        menu_choice = IO.input_menu_choice()
        match menu_choice:

            # Input user data
            case "1":
                students = IO.input_student_data(student_data=students)
                print("\nData entered!")
                continue                            

            # Displays current data
            case "2":
                # Process the data to create and display a custom message
                IO.output_student_courses(student_data=students)
                
            # Saves data to the json file
            case "3":
                FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
                continue

            # Stops the program
            case "4":
                print("Program Ended")
                exit()