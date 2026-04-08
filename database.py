import mysql.connector
from mysql.connector import Error

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
            cls._instance.connect()
        return cls._instance

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='emp_management',
                user='root',
                password='Mysql@2004'
            )
        except Error as e:
            print(f"Error connecting to database: {e}")

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        self.connection.commit()
        return cursor

    def fetch_all(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        return cursor.fetchall()

    def fetch_one(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        return cursor.fetchone()