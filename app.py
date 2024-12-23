from tkinter import *
from tkinter import ttk, messagebox

from db import DataBase

from add import AddData
from view import ViewData
from report import ReportData


class App(Tk):

    def __init__(self, is_admin):
        super().__init__()

        ttk.Style().theme_use('clam')

        #self.geometry('500x500')

        self.db = DataBase()
        self.is_admin = is_admin

        frame = ttk.Frame(self, padding=20)

        btn_add = ttk.Button(frame, text='Добавить данные', command=self.open_add)
        btn_view = ttk.Button(frame, text='Функции администратора', command=self.open_view)
        btn_report = ttk.Button(frame, text='Отчет о стадионе', command=self.open_report)

        frame.pack(fill=BOTH)
        btn_add.pack(side=TOP, pady=5)
        btn_view.pack(side=TOP, pady=5)
        btn_report.pack(side=TOP, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.close)

    def run(self):
        return self.mainloop()
    
    def close(self):
        #self.db.close_connection()
        self.destroy()

    def open_add(self):
        try:
            self.add.deiconify()
        except:
            self.add = AddData(self) 

    def open_view(self):
        if not self.is_admin:
            messagebox.showerror("Error", "You are not an administrator.")
            return
        try:
            self.view.deiconify()
        except:
            self.view = ViewData(self)  

    def open_report(self):
        try:
            self.report.deiconify()
        except:
            self.report = ReportData(self) 