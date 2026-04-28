import tkinter as tk
from GUI.student_screen import StudentScreen
from Repository_Pattern.student_service import StudentService


class MainWindow:
    def __init__(self, root, student_service: StudentService):
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("800x600")

        self.student_service = student_service

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="School System", font=("Arial", 20))
        title.pack(pady=20)

        btn_students = tk.Button(
            self.root,
            text="Manage Students",
            width=20,
            height=2,
            command=self.open_students
        )
        btn_students.pack(pady=10)

    def open_students(self):
        StudentScreen(self.root, self.student_service)