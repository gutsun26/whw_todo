'''
Created on Nov 12, 2026

@author: Sunder B
'''
from datetime import date, timedelta

class TaskModel:
    def __init__(self, db_manager):
        self.db = db_manager

    def add_task(self, text, task_date):
        query = "INSERT INTO tasks (task_text, task_date, status) VALUES (%s, %s, 'PENDING')"
        self.db.execute_query(query, (text, task_date))

    def update_task_status(self, task_id, status):
        query = "UPDATE tasks SET status = %s WHERE id = %s"
        self.db.execute_query(query, (status, task_id))

    def update_task_text(self, task_id, new_text):
        query = "UPDATE tasks SET task_text = %s WHERE id = %s"
        self.db.execute_query(query, (new_text, task_id))

    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = %s"
        self.db.execute_query(query, (task_id,))

    def get_tasks_by_date(self, task_date):
        query = "SELECT id, task_text, status FROM tasks WHERE task_date = %s"
        return self.db.fetch_query(query, (task_date,))

    def carry_forward_pending_tasks(self, today_date):
        """Automatically carry forward unresolved tasks from past dates to today."""
        query = """
            UPDATE tasks 
            SET task_date = %s 
            WHERE status = 'PENDING' AND task_date < %s
        """
        self.db.execute_query(query, (today_date, today_date))

    def get_dashboard_stats(self, days_ago, today_date):
        start_date = today_date - timedelta(days=days_ago)
        query = """
            SELECT status, COUNT(*) as count 
            FROM tasks 
            WHERE task_date BETWEEN %s AND %s 
            GROUP BY status
        """
        results = self.db.fetch_query(query, (start_date, today_date))
        stats = {"DONE": 0, "PENDING": 0, "CANCELLED": 0}
        for row in results:
            stats[row["status"]] = row["count"]
        return stats