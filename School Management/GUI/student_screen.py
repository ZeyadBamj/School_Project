import tkinter as tk
from tkinter import messagebox
from validator import InputValidator as Valid
from GUI.update_window import UpdateWindow
from Repository_Pattern.student_service import StudentService


class StudentScreen:
    def __init__(self, root, student_service: StudentService):
        self.student_service = student_service

        self.window = tk.Toplevel(root)
        self.window.title("Student Management")
        self.window.geometry("500x600")

        self.window.transient(root)
        self.window.grab_set()
        self.window.focus_force()

        self.create_widgets()

    # ================= UI =================
    def create_widgets(self):
        tk.Label(self.window, text="Student ID").pack()
        self.id_entry = tk.Entry(self.window)
        self.id_entry.pack()

        tk.Label(self.window, text="First Name").pack()
        self.first_entry = tk.Entry(self.window)
        self.first_entry.pack()

        tk.Label(self.window, text="Last Name").pack()
        self.last_entry = tk.Entry(self.window)
        self.last_entry.pack()

        tk.Label(self.window, text="Age").pack()
        self.age_entry = tk.Entry(self.window)
        self.age_entry.pack()

        tk.Label(self.window, text="Grade").pack()
        self.grade_entry = tk.Entry(self.window)
        self.grade_entry.pack()

        tk.Label(self.window, text="Registration Date (DD-MM-YYYY)").pack()
        self.date_entry = tk.Entry(self.window)
        self.date_entry.pack()

        tk.Label(self.window, text="Lessons (comma separated)").pack()
        self.lessons_entry = tk.Entry(self.window)
        self.lessons_entry.pack()

        # ===== Buttons =====
        tk.Button(self.window, text="Add Student", command=self.add_student).pack(pady=5)
        tk.Button(self.window, text="Delete Student By ID", command=self.delete_student).pack(pady=5)
        tk.Button(self.window, text="Update Student By ID", command=self.update_student).pack(pady=5)
        tk.Button(self.window, text="Show Student By ID", command=self.show_student).pack(pady=5)

        # ===== Output =====
        self.output = tk.Text(self.window, height=10)
        self.output.pack(pady=10)

    #================ CLEAR FIELDS & KEEP STUDENT MANAGEMENT ON TOP MAIN WINDOW =============
    def clear_fields(self):
        for entry in [
            self.id_entry,
            self.first_entry,
            self.last_entry,
            self.age_entry,
            self.grade_entry,
            self.date_entry,
            self.lessons_entry
        ]:
            entry.delete(0, tk.END)

    def keep_on_top(self):
        self.window.lift()
        self.window.focus_force()

    # ================= ADD =================
    def add_student(self):
        try:
            data = (
                int(self.id_entry.get()),
                self.first_entry.get(),
                self.last_entry.get(),
                int(self.age_entry.get()),
                self.grade_entry.get(),
                Valid.gui_date_input(self.date_entry.get()),
            )

            lessons = self.lessons_entry.get().split(',')

            success, message = self.student_service.add_student(data, lessons)

            messagebox.showinfo("Result", message)

            if success:
                self.clear_fields()

            self.keep_on_top()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.keep_on_top()

    # ================= DELETE =================
    def delete_student(self):
        try:
            student_id = int(self.id_entry.get())
            success, message = self.student_service.delete_student(student_id)

            messagebox.showinfo("Result", message)

            if success:
                self.clear_fields()

            self.keep_on_top()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.keep_on_top()

    # ================= UPDATE =================
    def update_student(self):
        try:
            student_id = int(self.id_entry.get())

            result = self.student_service.get_student_info(student_id)

            if not result:
                messagebox.showerror("Error", "Student not found")
                self.keep_on_top()
                return

            student, _ = result

            UpdateWindow(self.window, self.student_service, student_id, student)

            self.keep_on_top()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.keep_on_top()

    # ================= SHOW =================
    def show_student(self):
        try:
            student_id = int(self.id_entry.get())
            result = self.student_service.get_student_info(student_id)

            self.output.delete("1.0", tk.END)

            if result:
                student, lessons = result

                text = f"""
ID: {student.student_id}
First Name: {student.first_name}
Last Name: {student.last_name}
Age: {student.age}
Grade: {student.grade}
Registration Date: {student.registration_date}
Lessons: [{', '.join(lessons) if lessons else "No Lessons"}]
"""
                self.output.insert(tk.END, text)

            else:
                self.output.insert(tk.END, "\nStudent Not Found")

        except Exception as e:
            self.output.insert(tk.END, f"\nError: {str(e)}", )
