import unittest
from unittest import TestCase
from DB_and_Related.database import DataBase
from DB_and_Related.model import Model
from DB_and_Related.tables import Lessons, Student_lessons
from Repository_Pattern.lesson_repo import LessonRepository


class TestLessonRepository(TestCase):
    def setUp(self):
        self.db_path = ":memory:"
        Model.db = DataBase(self.db_path)
        Model.connection = Model.db.connect()

        Lessons.create_table()
        Student_lessons.create_table()
        self.repo = LessonRepository(self.db_path)

        print("SETUP RUNNING")

    def tearDown(self):
        if Model.connection:
            Model.connection.close()

    def test_get_or_create_new_lesson(self):
        lesson_id = self.repo.get_or_create('Math')

        cursor = Model.connection.cursor()
        cursor.execute("SELECT name FROM lessons WHERE id = ?", (lesson_id,))
        row = cursor.fetchone()

        self.assertIsInstance(lesson_id, int)
        self.assertEqual(row['name'], 'Math')

    def test_get_or_create_existing(self):
        cursor = Model.connection.cursor()
        cursor.execute('INSERT INTO lessons (name) VALUES (?)',
                       ("English",))
        Model.connection.commit()

        id1 = self.repo.get_or_create('English')
        id2 = self.repo.get_or_create('English')

        self.assertEqual(id1, id2)

    def test_assign_to_student(self):
        cursor = Model.connection.cursor()
        cursor.execute('INSERT INTO lessons (name) VALUES (?)',
                       ("Arabic",))
        lesson_id = cursor.lastrowid
        Model.connection.commit()

        self.repo.assign_to_student(1, lesson_id)
        cursor.execute('SELECT * FROM student_lessons WHERE student_id = 1')
        rows = cursor.fetchall()

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['lesson_id'], lesson_id)

    def test_get_by_student(self):
        cursor = Model.connection.cursor()
        cursor.execute("INSERT INTO lessons (name) VALUES (?)", ("Math",))
        lesson1 = cursor.lastrowid
        cursor.execute("INSERT INTO lessons (name) VALUES (?)", ("English",))
        lesson2 = cursor.lastrowid
        Model.connection.commit()

        self.repo.assign_to_student(1, lesson1)
        self.repo.assign_to_student(1, lesson2)
        result = self.repo.get_by_student(1)

        self.assertIn("Math", result)
        self.assertIn("English", result)
        self.assertEqual(len(result), 2)

    def test_clear_student_lessons(self):
        cursor = Model.connection.cursor()
        cursor.execute("INSERT INTO lessons (name) VALUES (?)", ('Math',))
        lesson_id = cursor.lastrowid
        Model.connection.commit()

        self.repo.assign_to_student(1, lesson_id)
        self.repo.clear_student_lessons(1)
        cursor.execute('SELECT * FROM student_lessons WHERE student_id = 1')
        rows = cursor.fetchall()

        self.assertEqual(len(rows), 0)

if __name__ == "__main__":
    unittest.main()