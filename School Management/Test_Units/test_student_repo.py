import random
import unittest
from unittest import TestCase
from DB_and_Related.database import DataBase
from DB_and_Related.model import Model
from DB_and_Related.tables import Students
from Repository_Pattern.student_repo import StudentRepository

class TestStudentRepository(TestCase):
    def setUp(self):
        self.db_path = ":memory:"
        Model.db = DataBase(self.db_path)
        Model.connection = Model.db.connect()

        Students.create_table()
        self.repo = StudentRepository(self.db_path)

        print("SETUP RUNNING")

    def tearDown(self):
       if Model.connection:
           Model.connection.close()

    def test_add_student(self):
        student = Students(
            student_id= random.randint(1, 10000),
            first_name="Ali",
            last_name="Test",
            age=20,
            grade="A",
            registration_date="2026-04-27"
        )

        student_id = self.repo.add(student)

        self.assertIsNotNone(student_id)

    def test_exists(self):
        student = Students(
            student_id= random.randint(1, 10000),
            first_name="Salem",
            last_name="Ghaleb",
            age=30,
            grade="B",
            registration_date="2026-04-27"
        )

        self.repo.add(student)

        self.assertTrue(self.repo.exists(student.student_id))

    def test_delete(self):
        student = Students(
            student_id= random.randint(1, 10000),
            first_name="Saleh",
            last_name="Ghaleb",
            age=30,
            grade="B",
            registration_date="2026-04-27"
        )

        self.repo.add(student)
        self.repo.delete(student.student_id)

        self.assertFalse(self.repo.exists(student.student_id))

    def test_update(self):
        student = Students(
            student_id=random.randint(1, 10000),
            first_name="Saleh",
            last_name="Ghaleb",
            age=30,
            grade="B",
            registration_date="2026-04-27"
        )

        self.repo.add(student)
        student.first_name = 'UpdatedName'
        student.age = 50
        self.repo.update(student)
        updated = self.repo.get_by_student_id(student.student_id)

        self.assertEqual(updated.first_name, "UpdatedName")
        self.assertEqual(updated.age, 50)

    def test_get_by_student_id(self):
        student = Students(
            student_id=random.randint(1, 10000),
            first_name="Yzeed",
            last_name="Ghaleb",
            age=60,
            grade="B",
            registration_date="2026-04-27"
        )

        self.repo.add(student)
        student_info = self.repo.get_by_student_id(student.student_id)

        self.assertIsNotNone(student_info)


if __name__ == "__main__":
    unittest.main()
