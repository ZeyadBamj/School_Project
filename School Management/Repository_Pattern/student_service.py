from DB_and_Related.tables import Students
from Repository_Pattern.lesson_repo import LessonRepository
from Repository_Pattern.student_repo import StudentRepository


class StudentService:
    def __init__(self, student_repo: StudentRepository, lesson_repo: LessonRepository):
        self.student_repo = student_repo
        self.lesson_repo = lesson_repo

    def add_student(self, data, lesson_list):
        student_id = data[0]
        if self.student_repo.exists(student_id):
            return False, "❌ Can't ADD, Student Exists Before"

        student_obj = Students(student_id=data[0], first_name=data[1], last_name=data[2],
                               age=data[3], grade=data[4], registration_date=data[5])
        self.student_repo.add(student_obj)
        student_pk_id  = self.student_repo.get_pk_by_student_id(student_id)

        for lesson_name in lesson_list:
            lesson_name = lesson_name.strip()
            if not lesson_name: continue
            lesson_id = self.lesson_repo.get_or_create(lesson_name)
            self.lesson_repo.assign_to_student(student_pk_id, lesson_id)

        return True, "✅ ADD Successfully"

    def delete_student(self, student_id):
        student = self.student_repo.get_by_student_id(student_id)
        if not student:
            return False, "❌ Student Not Found"

        self.lesson_repo.clear_student_lessons(student_id)
        self.student_repo.delete(student_id)
        return True, "✅ DELETED Successfully"

    def update_student(self, student_id, get_input_func):
        student = self.student_repo.get_by_student_id(student_id)
        if not student:
            return False, "❌ Student Not Found"

        new_data = get_input_func(student)
        student.first_name = new_data['first_name'] or student.first_name
        student.last_name = new_data['last_name'] or student.last_name
        student.age = new_data['age'] or student.age
        student.grade = new_data['grade'] or student.grade
        student.registration_date = new_data['registration_date'] or student.registration_date

        self.student_repo.update(student)
        return True, "✅ UPDATED Student Information Successfully"

    def get_student_info(self, student_id):
        student = self.student_repo.get_by_student_id(student_id)
        if not student:
            return None

        lessons = self.lesson_repo.get_by_student(student_id)
        return student, lessons
