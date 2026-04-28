import tkinter as tk
from tkinter import messagebox


class UpdateWindow:
    def __init__(self, root, service, student_id, student):
        self.service = service
        self.student_id = student_id

        self.win = tk.Toplevel(root)
        self.win.title("Update Student")

        self.first = self.create_entry("First Name", student.first_name)
        self.last = self.create_entry("Last Name", student.last_name)
        self.age = self.create_entry("Age", student.age)
        self.grade = self.create_entry("Grade", student.grade)
        self.date = self.create_entry("Registration Date", student.registration_date)

        tk.Button(self.win, text="Save", command=self.save).pack(pady=10)

    def create_entry(self, label, value):
        tk.Label(self.win, text=label).pack()
        e = tk.Entry(self.win)
        e.insert(0, value)
        e.pack()
        return e

    def save(self):
        def get_updated_input(student):
            return {
                "first_name": self.first.get() or student.first_name,
                "last_name": self.last.get() or student.last_name,
                "age": int(self.age.get()) if self.age.get() else student.age,
                "grade": self.grade.get() or student.grade,
                "registration_date": self.date.get() or student.registration_date
            }

        success, message = self.service.update_student(self.student_id, get_updated_input)

        messagebox.showinfo("Result", message)
        self.win.destroy()

        self.win.master.lift()
        self.win.master.focus_force()
