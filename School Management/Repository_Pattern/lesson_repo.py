from abc import ABC, abstractmethod
from DB_and_Related.model import Model


class ILessonRepository(ABC):
    @abstractmethod
    def get_or_create(self, lesson_name):
        pass

    @abstractmethod
    def assign_to_student(self, student_pk_id, lesson_id):
        pass

    @abstractmethod
    def get_by_student(self, student_pk_id):
        pass

    @abstractmethod
    def clear_student_lessons(self, student_pk_id):
        pass

class LessonRepository(ILessonRepository):
    def __init__(self, db_path='school_management.db'):
        self.db_path = db_path

    @staticmethod
    def _get_conn_and_cursor():
        if Model.connection is None:
            raise Exception("❌ Database connection is not initialized")
        return Model.connection, Model.connection.cursor()

    def get_or_create(self, lesson_name):
        conn, cursor = self._get_conn_and_cursor()
        cursor.execute("SELECT id FROM lessons WHERE name = ?", (lesson_name,))
        row = cursor.fetchone()

        if row:
            result = row[0]
        else:
            cursor.execute("INSERT INTO lessons (name) VALUES (?)", (lesson_name,))
            result = cursor.lastrowid

        return result

    def assign_to_student(self, student_pk_id, lesson_id):
        conn, cursor = self._get_conn_and_cursor()
        cursor.execute("INSERT INTO student_lessons (student_id, lesson_id) "
                       "VALUES (?, ?)", (student_pk_id, lesson_id))

    def get_by_student(self, student_id):
        conn, cursor = self._get_conn_and_cursor()
        cursor.execute("""SELECT l.name FROM lessons l
            JOIN student_lessons sl ON l.id = sl.lesson_id
            WHERE sl.student_id = (
            SELECT id FROM students WHERE student_id = ?
            )""", (student_id,))
        lessons = [row[0] for row in cursor.fetchall()]
        return lessons

    def clear_student_lessons(self, student_id):
        conn, cursor = self._get_conn_and_cursor()
        cursor.execute("DELETE FROM student_lessons WHERE student_id = ( SELECT id FROM students WHERE student_id = ? )", (student_id,))
