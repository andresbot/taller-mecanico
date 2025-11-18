import mysql.connector
from mysql.connector import Error

class DatabaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    user="root",
                    password="root",
                    host="127.0.0.1",
                    database="registrodb",
                    port="3306"
                )
            return self.connection
        except Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def execute_query(self, query, params=None):
        try:
            connection = self.connect()
            cursor = connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.lower().strip().startswith('select'):
                result = cursor.fetchall()
            else:
                connection.commit()
                result = cursor.lastrowid
            
            cursor.close()
            if not query.lower().strip().startswith('select'):
                connection.close()
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            raise

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()