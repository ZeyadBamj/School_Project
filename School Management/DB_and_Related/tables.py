from DB_and_Related.fields import IntegerField, CharField, ForeignKeyField
from DB_and_Related.model import Model

class Students(Model):
    student_id = IntegerField(unique=True, nullable=False)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    age = IntegerField()
    grade = CharField(max_length=30)
    registration_date = CharField()

class Lessons(Model):
    name = CharField(max_length=100, unique=True, nullable=False)

class Student_lessons(Model):
    student_id = ForeignKeyField(Students)
    lesson_id = ForeignKeyField(Lessons)

    @classmethod
    def get_table_constraints(cls):
        return [
            "UNIQUE(student_id, lesson_id)"
        ]