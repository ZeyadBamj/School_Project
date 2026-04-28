import sqlite3

class DataBase:
    def __init__(self, path):
        self.path = path
        self.connection = None
        self.connected = False
        self.connect()

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.path)
            self.connection.row_factory = sqlite3.Row
            self.connected = True
        except sqlite3.Error as e:
            print(f"❌ Database connection error: {e}")
            self.connected = False
        return self.connection

    def commit(self):
        if self.connected and self.connection:
            try:
                self.connection.commit()
            except sqlite3.Error as e:
                print(f"❌ Error committing transaction: {e}")

    def close(self):
        if self.connected and self.connection:
            try:
                self.connection.close()
            except sqlite3.Error as e:
                pass
        self.connected = False