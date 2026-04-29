from DB_and_Related.database import DataBase
from DB_and_Related.model import Model
from DB_and_Related.tables import Students, Lessons, Student_lessons
from Repository_Pattern.lesson_repo import LessonRepository
from Repository_Pattern.student_repo import StudentRepository
from Repository_Pattern.student_service import StudentService
from validator import InputValidator
import tkinter as tk
from GUI.main_window import MainWindow

DB_PATH = 'school_management.db'
Model.db = DataBase(DB_PATH)
Model.connection = Model.db.connect()
Model.connection.execute("PRAGMA foreign_keys = ON")

Students.create_table()
Lessons.create_table()
Student_lessons.create_table()


def main():
    student_repo = StudentRepository(DB_PATH)
    lesson_repo = LessonRepository(DB_PATH)
    service = StudentService(student_repo, lesson_repo)

    root = tk.Tk()
    MainWindow(root, service)

    root.mainloop()


    while True:
        print("""\n--- Main List ---
(a) -> ADD Student
(d) -> DELETE Student
(u) -> UPDATE Student Information
(s) -> SHOW Student Information
(q) -> EXIT""")

        choice = input("Please Choose the letter of the process:\n").lower().strip()

        if choice == 'a':
            add_student_main(service)

        elif choice == 'd':
            delete_student_main(service)

        elif choice == 'u':
            update_student_main(service)

        elif choice == 's':
            show_student_info_main(service)

        elif choice == 'q':
            print("END Program...")
            break

        else:
            print("❌ Wrong Choice")


def add_student_main(service: StudentService):
    validator = InputValidator()
    try:
        student_id = validator.int_input("Student ID: ")
        f_name = validator.str_input("First Name: ")
        l_name = validator.str_input("Last Name: ")
        age = validator.int_input("Age: ")
        grade = validator.str_input("Grade: ")
        reg_date = validator.date_input("Registration Date (DD-MM-YYYY): ")

        lessons_str = validator.str_input("Enter lessons (with comma between them): ")
        lessons_list = lessons_str.split(',')

        data = (student_id, f_name, l_name, age, grade, reg_date)
        success, message = service.add_student(data, lessons_list)
        print(message)
    except ValueError:
        print("❌ Error, some input is wrong")


def delete_student_main(service: StudentService):
    try:
        student_id = int(input("Enter Student ID: "))
        success, message = service.delete_student(student_id)
        print(message)
    except ValueError:
        print("❌ Invalid input (check numbers or empty fields)")


def get_update_input(student: Students):
    validator = InputValidator()

    print(f"""
Current Data:
First Name: {student.first_name}
Last Name: {student.last_name}
Age: {student.age}
Grade: {student.grade}
Registration Date: {student.registration_date}
""")

    return {
        "first_name": validator.str_input(
            f"({student.first_name}) New First Name: ",
            allow_empty=True,
            default=student.first_name
        ),

        "last_name": validator.str_input(
            f"({student.last_name}) New Last Name: ",
            allow_empty=True,
            default=student.last_name
        ),

        "age": validator.int_input(
            f"({student.age}) New Age: ",
            allow_empty=True,
            default=student.age
        ),

        "grade": validator.str_input(
            f"({student.grade}) New Grade: ",
            allow_empty=True,
            default=student.grade
        ),

        "registration_date": validator.date_input(
            f"({student.registration_date}) New Date: ",
            allow_empty=True,
            default=student.registration_date
        )
    }


def update_student_main(service: StudentService):
    try:
        student_id = int(input("Enter Student ID: "))
        success, message = service.update_student(student_id, get_update_input)
        print(message)
    except ValueError:
        print("❌ Invalid input (check numbers or empty fields)")


def show_student_info_main(service: StudentService):
    try:
        student_id = int(input("Enter Student ID: "))
        result = service.get_student_info(student_id)
        if result:
            student, lessons = result
            print(
                f"""\n--- Student Information ---
ID: {student.student_id}
First Name: {student.first_name}
Last Name: {student.last_name}
Age: {student.age}
Grade: {student.grade}
Registration Date: {student.registration_date}
Lessons: [{', '.join(lessons) if lessons else "No Lesson"}]"""
            )
        else:
            print("❌ Student Not Exists")
    except ValueError:
        print("❌ Invalid input (check numbers or empty fields)")

if __name__ == "__main__":
    try:
        main()
    finally:
        if Model.connection:
            Model.connection.close()
