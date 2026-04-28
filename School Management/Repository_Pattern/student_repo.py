from abc import ABC, abstractmethod
from DB_and_Related.model import Model
from DB_and_Related.tables import Students


class IStudentRepository(ABC):
    @abstractmethod
    def add(self, student_obj):
        pass

    @abstractmethod
    def delete(self, student_id):
        pass

    @abstractmethod
    def update(self, student_obj):
        pass

    @abstractmethod
    def get_by_student_id(self, student_id):
        pass

    @abstractmethod
    def exists(self, student_id):
        pass

    @abstractmethod
    def get_pk_by_student_id(self, student_id):
        pass


class StudentRepository(IStudentRepository):
    def __init__(self, db_path='school_management.db'):
        self.db_path = db_path

    @staticmethod
    def _get_conn_and_cursor():
        if Model.connection is None:
            raise Exception("❌ Database connection is not initialized")
        return Model.connection, Model.connection.cursor()

    def exists(self, student_id):
        conn, cursor = self._get_conn_and_cursor()
        cursor.execute("SELECT 1 FROM students WHERE student_id = ?", (student_id,))
        exists = cursor.fetchone() is not None
        return exists

    def add(self, s: Students):
        conn, cursor = self._get_conn_and_cursor()
        cursor.execute("""
            INSERT INTO students (student_id, first_name, last_name, age, grade, registration_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (s.student_id, s.first_name, s.last_name, s.age, s.grade, s.registration_date))
        last_id = cursor.lastrowid
        conn.commit()
        return last_id

    def delete(self, student_id):
        conn, cursor = self._get_conn_and_cursor()
        cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        conn.commit()

    def update(self, s: Students):
        conn, cursor = self._get_conn_and_cursor()
        cursor.execute("""
            UPDATE students SET first_name=?, last_name=?, age=?, grade=?, registration_date=?
            WHERE student_id=?
        """, (s.first_name, s.last_name, s.age,
              s.grade, s.registration_date,
              s.student_id))
        conn.commit()

    def get_by_student_id(self, student_id):
        conn, cursor = self._get_conn_and_cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        row = cursor.fetchone()
        if row:
            return Students(id=row[0], student_id=row[1], first_name=row[2], last_name=row[3],
                            age=row[4], grade=row[5], registration_date=row[6])
        return None

    def get_pk_by_student_id(self, student_id):
        conn, cursor = self._get_conn_and_cursor()
        cursor.execute("SELECT id FROM students WHERE student_id = ?", (student_id,))
        row = cursor.fetchone()
        return row[0] if row else None
