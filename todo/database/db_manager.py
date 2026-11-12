'''
Created on Nov 12, 2026

@author: Sunder B
'''
import mysql.connector
from mysql.connector import Error

class DBManager:
    def __init__(self, host="localhost", user="root", password="root", database="todo_db"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.connect()
        self.create_table()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task_text VARCHAR(255) NOT NULL,
            task_date DATE NOT NULL,
            status ENUM('DONE', 'PENDING', 'CANCELLED') DEFAULT 'PENDING'
        )
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        self.connection.commit()
        cursor.close()

    def fetch_query(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        cursor.close()
        return result
    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = %s"
        self.db.execute_query(query, (task_id,))

    def update_task_text(self, task_id, new_text):
        query = "UPDATE tasks SET task_text = %s WHERE id = %s"
        self.db.execute_query(query, (new_text, task_id))