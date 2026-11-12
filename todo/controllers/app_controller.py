'''
Created on Nov 12, 2026

@author: Sunder B
'''
from datetime import date
from todo.database.db_manager import DBManager
from todo.models.task_model import TaskModel
from todo.views.main_window import MainWindow

class AppController:
    def __init__(self):
        self.db = DBManager()
        self.model = TaskModel(self.db)
        
        # Automatically carry forward pending tasks from previous days to today on startup
        self.model.carry_forward_pending_tasks(date.today())
        
        self.view = MainWindow(self)

    def run(self):
        self.view.mainloop()

    def get_tasks_for_date(self, task_date):
        return self.model.get_tasks_by_date(task_date)

    def save_new_task(self, text, task_date):
        self.model.add_task(text, task_date)

    def update_status(self, task_id, status):
        self.model.update_task_status(task_id, status)

    def get_stats(self, days):
        return self.model.get_dashboard_stats(days, date.today())
    def update_text(self, task_id, new_text):
        self.model.update_task_text(task_id, new_text)

    def remove_task(self, task_id):
        self.model.delete_task(task_id)