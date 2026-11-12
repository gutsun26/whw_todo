'''
Created on Nov 12, 2026

@author: Sunder B
'''
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date

class TodoTab(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Top Frame for Date Selection
        top_frame = ttk.Frame(self, padding=10)
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="Select Date:").pack(side=tk.LEFT, padx=5)
        self.date_picker = DateEntry(top_frame, width=12, background='darkblue',
                                     foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_picker.pack(side=tk.LEFT, padx=5)
        self.date_picker.set_date(date.today())
        self.date_picker.bind("<<DateEntrySelected>>", self.on_date_changed)

        ttk.Button(top_frame, text="Load Tasks", command=self.load_tasks).pack(side=tk.LEFT, padx=10)
        ttk.Button(top_frame, text="+ Add New Task", command=self.add_task_row).pack(side=tk.RIGHT, padx=5)

        # Scrollable Task Container
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.task_frame = ttk.Frame(self.canvas, padding=10)

        self.task_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.task_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_widgets = []
        self.load_tasks()

    def on_date_changed(self, event=None):
        self.load_tasks()

    def load_tasks(self):
        for widget in self.task_widgets:
            widget.destroy()
        self.task_widgets.clear()

        selected_date = self.date_picker.get_date()
        tasks = self.controller.get_tasks_for_date(selected_date)

        if not tasks:
            self.add_task_row()
        else:
            for task in tasks:
                self.create_task_widget(task['id'], task['task_text'], task['status'])

    def create_task_widget(self, task_id, text, status):
        # Use tk.Frame instead of ttk.Frame to allow custom background coloring
        bg_color = "#FFF3CD" if status == "PENDING" else "#F8F9FA"  # Soft yellow for PENDING
        
        row_frame = tk.Frame(self.task_frame, bg=bg_color, padx=5, pady=5, bd=1, relief="solid")
        row_frame.pack(fill=tk.X, expand=True, pady=3)

        # Task Text Label (or Entry when editing)
        task_label = tk.Label(row_frame, text=text, width=35, anchor="w", bg=bg_color, font=("Arial", 10))
        task_label.pack(side=tk.LEFT, padx=5)

        status_var = tk.StringVar(value=status)

        # Radiobuttons for Status update
        for st in ["DONE", "PENDING", "CANCELLED"]:
            rb = ttk.Radiobutton(
                row_frame, text=st, value=st, variable=status_var,
                command=lambda tid=task_id, var=status_var: self.controller.update_status(tid, var.get())
            )
            rb.pack(side=tk.LEFT, padx=2)

        # Edit Button functionality
        def enable_edit():
            task_label.pack_forget()
            edit_entry = tk.Entry(row_frame, width=33, font=("Arial", 10))
            edit_entry.insert(0, text)
            edit_entry.pack(side=tk.LEFT, padx=5)
            
            edit_btn.pack_forget()
            
            def save_edit():
                new_text = edit_entry.get().strip()
                if new_text:
                    self.controller.update_text(task_id, new_text)
                    self.load_tasks()

            save_btn = ttk.Button(row_frame, text="Update", command=save_edit)
            save_btn.pack(side=tk.LEFT, padx=2)

        edit_btn = ttk.Button(row_frame, text="Edit", width=6, command=enable_edit)
        edit_btn.pack(side=tk.LEFT, padx=5)

        # Delete Button functionality
        def delete_task():
            self.controller.remove_task(task_id)
            self.load_tasks()

        del_btn = ttk.Button(row_frame, text="Delete", width=6, command=delete_task)
        del_btn.pack(side=tk.LEFT, padx=5)

        self.task_widgets.append(row_frame)

    def add_task_row(self):
        row_frame = tk.Frame(self.task_frame, bg="#FFFFFF", padx=5, pady=5, bd=1, relief="solid")
        row_frame.pack(fill=tk.X, expand=True, pady=3)

        task_entry = tk.Entry(row_frame, width=42, font=("Arial", 10))
        task_entry.pack(side=tk.LEFT, padx=5)

        def save_task():
            txt = task_entry.get().strip()
            sel_date = self.date_picker.get_date()
            if txt:
                self.controller.save_new_task(txt, sel_date)
                self.load_tasks()

        ttk.Button(row_frame, text="Save", command=save_task).pack(side=tk.LEFT, padx=5)
        self.task_widgets.append(row_frame)