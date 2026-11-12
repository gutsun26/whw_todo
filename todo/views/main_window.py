'''
Created on Nov 12, 2026

@author: Sunder B
'''
import tkinter as tk
from tkinter import ttk
from todo.views.todo_tab import TodoTab
from todo.views.dashboard_tab import DashboardTab

class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Modular Daily Todo Desktop App")
        self.geometry("750x500")

        # Main Notebook (Tabs)
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.todo_tab = TodoTab(notebook, controller)
        self.dashboard_tab = DashboardTab(notebook, controller)

        notebook.add(self.todo_tab, text="Daily Todo")
        notebook.add(self.dashboard_tab, text="Dashboard")