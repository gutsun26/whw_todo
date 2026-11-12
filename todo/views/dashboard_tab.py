'''
Created on Nov 12, 2026

@author: Sunder B
'''
import tkinter as tk
from tkinter import ttk

class DashboardTab(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Task Analytics Dashboard", font=("Arial", 16, "bold")).pack(pady=10)

        self.frames = {}
        for period in [("Week (Last 7 Days)", 7), ("Month (Last 30 Days)", 30), ("6 Months (Last 180 Days)", 180)]:
            frame = ttk.LabelFrame(self, text=period[0], padding=15)
            frame.pack(fill=tk.X, padx=20, pady=10)
            
            lbl = ttk.Label(frame, text="Loading...", font=("Arial", 11))
            lbl.pack(anchor="w")
            self.frames[period[1]] = lbl

        ttk.Button(self, text="Refresh Dashboard", command=self.refresh_data).pack(pady=10)
        self.refresh_data()

    def refresh_data(self):
        for days, label in self.frames.items():
            stats = self.controller.get_stats(days)
            text = f"✅ DONE: {stats['DONE']}   |   ⏳ PENDING: {stats['PENDING']}   |   ❌ CANCELLED: {stats['CANCELLED']}"
            label.config(text=text)