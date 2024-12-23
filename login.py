import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from app import App

class Login:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x300")
        self.root.title("Login System")
        self.login_page()

    def login_page(self):
        # Создание экрана для входа
        self.clear_screen()  # Очистить экран, если это необходимо
        self.login_label = tk.Label(self.root, text="Login", font=("Arial", 24))
        self.login_label.pack(pady=20)

        # Ввод логина
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        # Ввод пароля
        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        # Кнопка для входа
        self.login_button = tk.Button(self.root, text="Login", command=self.authenticate_user)
        self.login_button.pack(pady=10)

    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Проверка логина и пароля (для тестирования, в реальной ситуации логины и пароли могут быть из БД)
        if username == "admin" and password == "1234":  # Пример аутентификации
            self.open_main_page(permission=1)
        elif username == 'user' and password == '1234':
            self.open_main_page(permission=0)
        else:
            messagebox.showerror("Error", "Invalid credentials, please try again.")

    def open_main_page(self, permission):
        # Переключение на главный интерфейс после успешной аутентификации
        self.root.destroy()
        App(permission).run()
        # Здесь можно вызвать другие окна для функционала приложения

    def clear_screen(self):
        # Очищаем экран
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

