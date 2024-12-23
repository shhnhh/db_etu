import tkinter as tk
from tkinter import messagebox, ttk

class ViewData(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app)
        self.db = app.db  # доступ к базе данных
        self.title("Football Database Viewer")
        self.geometry("1000x600")
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)
        self.create_tabs()

    def create_tabs(self):
        # Создаем вкладки для каждой таблицы
        self.team_tab = ttk.Frame(self.tabs)
        self.player_tab = ttk.Frame(self.tabs)
        self.stadium_tab = ttk.Frame(self.tabs)
        self.match_tab = ttk.Frame(self.tabs)
        self.performance_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.team_tab, text="Teams")
        self.tabs.add(self.player_tab, text="Players")
        self.tabs.add(self.stadium_tab, text="Stadiums")
        self.tabs.add(self.match_tab, text="Matches")
        self.tabs.add(self.performance_tab, text="Performance")

        # Создание табов с таблицами
        self.create_team_tab()
        self.create_player_tab()
        self.create_stadium_tab()
        self.create_match_tab()
        self.create_performance_tab()

    def create_team_tab(self):
        columns = ("ID", "Name", "City", "Coach", "Last Season Rank")
        self.team_table = ttk.Treeview(self.team_tab, columns=columns, show="headings")
        for col in columns:
            self.team_table.heading(col, text=col)
        self.team_table.pack(fill="both", expand=True)

        # Поле для поиска
        search_label = ttk.Label(self.team_tab, text="Search Team:")
        search_label.pack(padx=5, pady=5, anchor="w")
        self.search_entry = ttk.Entry(self.team_tab)
        self.search_entry.pack(fill="x", padx=5)
        ttk.Button(self.team_tab, text="Search", command=self.search_team).pack(pady=10)
        ttk.Button(self.team_tab, text="Load Teams", command=self.load_teams).pack(pady=10)
        ttk.Button(self.team_tab, text="Delete Selected Team", command=self.delete_team).pack(pady=10)

    def load_teams(self):
        query = "SELECT id, name, city, coach_name, last_season_rank FROM Teams"
        records = self.db.fetch_data(query)
        self.populate_table(self.team_table, records)

    def search_team(self):
        search_term = self.search_entry.get().lower()  # Считываем текст из поля поиска и преобразуем в нижний регистр
        query = f"SELECT id, name, city, coach_name, last_season_rank FROM Teams WHERE name LIKE '%{search_term}%'"
        records = self.db.fetch_data(query)
        self.populate_table(self.team_table, records)

    def create_player_tab(self):
        columns = ("ID", "Full Name", "Jersey Number", "Team ID")
        self.player_table = ttk.Treeview(self.player_tab, columns=columns, show="headings")
        for col in columns:
            self.player_table.heading(col, text=col)
        self.player_table.pack(fill="both", expand=True)

        # Поле для поиска
        search_label = ttk.Label(self.player_tab, text="Search Player:")
        search_label.pack(padx=5, pady=5, anchor="w")
        self.player_search_entry = ttk.Entry(self.player_tab)
        self.player_search_entry.pack(fill="x", padx=5)
        ttk.Button(self.player_tab, text="Search", command=self.search_player).pack(pady=10)
        ttk.Button(self.player_tab, text="Load Players", command=self.load_players).pack(pady=10)
        ttk.Button(self.player_tab, text="Delete Selected Player", command=self.delete_player).pack(pady=10)

    def load_players(self):
        query = "SELECT id, full_name, jersey_number, team_id FROM Players"
        records = self.db.fetch_data(query)
        self.populate_table(self.player_table, records)

    def search_player(self):
        search_term = self.player_search_entry.get().lower()  # Считываем текст из поля поиска и преобразуем в нижний регистр
        query = f"SELECT id, full_name, jersey_number, team_id FROM Players WHERE full_name LIKE '%{search_term}%'"
        records = self.db.fetch_data(query)
        self.populate_table(self.player_table, records)

    def create_stadium_tab(self):
        columns = ("ID", "Name", "City", "Capacity")
        self.stadium_table = ttk.Treeview(self.stadium_tab, columns=columns, show="headings")
        for col in columns:
            self.stadium_table.heading(col, text=col)
        self.stadium_table.pack(fill="both", expand=True)

        # Поле для поиска
        search_label = ttk.Label(self.stadium_tab, text="Search Stadium:")
        search_label.pack(padx=5, pady=5, anchor="w")
        self.stadium_search_entry = ttk.Entry(self.stadium_tab)
        self.stadium_search_entry.pack(fill="x", padx=5)
        ttk.Button(self.stadium_tab, text="Search", command=self.search_stadium).pack(pady=10)
        ttk.Button(self.stadium_tab, text="Load Stadiums", command=self.load_stadiums).pack(pady=10)
        ttk.Button(self.stadium_tab, text="Delete Selected Stadium", command=self.delete_stadium).pack(pady=10)

    def load_stadiums(self):
        query = "SELECT id, name, city, capacity FROM Stadiums"
        records = self.db.fetch_data(query)
        self.populate_table(self.stadium_table, records)

    def search_stadium(self):
        search_term = self.stadium_search_entry.get().lower()  # Считываем текст из поля поиска и преобразуем в нижний регистр
        query = f"SELECT id, name, city, capacity FROM Stadiums WHERE name LIKE '%{search_term}%'"
        records = self.db.fetch_data(query)
        self.populate_table(self.stadium_table, records)

    def create_match_tab(self):
        columns = ("ID", "Home Team", "Away Team", "Stadium", "Date", "Ticket Price")
        self.match_table = ttk.Treeview(self.match_tab, columns=columns, show="headings")
        for col in columns:
            self.match_table.heading(col, text=col)
        self.match_table.pack(fill="both", expand=True)

        # Поле для поиска
        search_label = ttk.Label(self.match_tab, text="Search Match:")
        search_label.pack(padx=5, pady=5, anchor="w")
        self.match_search_entry = ttk.Entry(self.match_tab)
        self.match_search_entry.pack(fill="x", padx=5)
        ttk.Button(self.match_tab, text="Search", command=self.search_match).pack(pady=10)
        ttk.Button(self.match_tab, text="Load Matches", command=self.load_matches).pack(pady=10)
        ttk.Button(self.match_tab, text="Delete Selected Match", command=self.delete_match).pack(pady=10)

    def load_matches(self):
        query = ("SELECT id, home_team_id, away_team_id, stadium_id, date, ticket_price FROM Matches")
        records = self.db.fetch_data(query)
        self.populate_table(self.match_table, records)

    def search_match(self):
        search_term = self.match_search_entry.get().lower()  # Считываем текст из поля поиска и преобразуем в нижний регистр
        query = f"SELECT id, home_team_id, away_team_id, stadium_id, date, ticket_price FROM Matches WHERE home_team_id LIKE '%{search_term}%' OR away_team_id LIKE '%{search_term}%'"
        records = self.db.fetch_data(query)
        self.populate_table(self.match_table, records)

    def create_performance_tab(self):
        columns = ("Match ID", "Player ID", "Goals")
        self.performance_table = ttk.Treeview(self.performance_tab, columns=columns, show="headings")
        for col in columns:
            self.performance_table.heading(col, text=col)
        self.performance_table.pack(fill="both", expand=True)

        # Поле для поиска
        search_label = ttk.Label(self.performance_tab, text="Search Performance:")
        search_label.pack(padx=5, pady=5, anchor="w")
        self.performance_search_entry = ttk.Entry(self.performance_tab)
        self.performance_search_entry.pack(fill="x", padx=5)
        ttk.Button(self.performance_tab, text="Search", command=self.search_performance).pack(pady=10)
        ttk.Button(self.performance_tab, text="Load Performance", command=self.load_performance).pack(pady=10)
        ttk.Button(self.performance_tab, text="Delete Selected Performance", command=self.delete_performance).pack(pady=10)

    def load_performance(self):
        query = "SELECT match_id, player_id, goals FROM Performance"
        records = self.db.fetch_data(query)
        self.populate_table(self.performance_table, records)

    def search_performance(self):
        search_term = self.performance_search_entry.get().lower()  # Считываем текст из поля поиска и преобразуем в нижний регистр
        query = f"SELECT match_id, player_id, goals FROM Performance WHERE player_id LIKE '%{search_term}%'"
        records = self.db.fetch_data(query)
        self.populate_table(self.performance_table, records)

    @staticmethod
    def populate_table(table, records):
        # Заполнение таблицы данными
        for row in table.get_children():
            table.delete(row)
        for record in records:
            table.insert("", "end", values=record)

    def delete_team(self):
        selected_item = self.team_table.selection()
        if selected_item:
            team_id = self.team_table.item(selected_item)["values"][0]
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the team with ID {team_id}?")
            if confirm:
                self.db.delete_team(team_id)
                self.team_table.delete(selected_item)
                messagebox.showinfo("Success", "Team successfully deleted!")
        else:
            messagebox.showwarning("Selection Error", "Please select a team to delete.")

    def delete_player(self):
        selected_item = self.player_table.selection()
        if selected_item:
            player_id = self.player_table.item(selected_item)["values"][0]
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the player with ID {player_id}?")
            if confirm:
                self.db.delete_player(player_id)
                self.player_table.delete(selected_item)
                messagebox.showinfo("Success", "Player successfully deleted!")
        else:
            messagebox.showwarning("Selection Error", "Please select a player to delete.")

    def delete_stadium(self):
        selected_item = self.stadium_table.selection()
        if selected_item:
            stadium_id = self.stadium_table.item(selected_item)["values"][0]
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the stadium with ID {stadium_id}?")
            if confirm:
                self.db.delete_stadium(stadium_id)
                self.stadium_table.delete(selected_item)
                messagebox.showinfo("Success", "Stadium successfully deleted!")
        else:
            messagebox.showwarning("Selection Error", "Please select a stadium to delete.")

    def delete_match(self):
        selected_item = self.match_table.selection()
        if selected_item:
            match_id = self.match_table.item(selected_item)["values"][0]
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the match with ID {match_id}?")
            if confirm:
                self.db.delete_match(match_id)
                self.match_table.delete(selected_item)
                messagebox.showinfo("Success", "Match successfully deleted!")
        else:
            messagebox.showwarning("Selection Error", "Please select a match to delete.")

    def delete_performance(self):
        selected_item = self.performance_table.selection()
        if selected_item:
            performance_id = self.performance_table.item(selected_item)["values"][0]
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the performance entry with Match ID {performance_id}?")
            if confirm:
                self.db.delete_performance(performance_id)
                self.performance_table.delete(selected_item)
                messagebox.showinfo("Success", "Performance entry successfully deleted!")
        else:
            messagebox.showwarning("Selection Error", "Please select a performance entry to delete.")

    def create_team_tab(self):
        columns = ("ID", "Name", "City", "Coach", "Last Season Rank")
        self.team_table = ttk.Treeview(self.team_tab, columns=columns, show="headings")
        for col in columns:
            self.team_table.heading(col, text=col)
        self.team_table.pack(fill="both", expand=True)

        # Поля поиска и кнопки
        search_label = ttk.Label(self.team_tab, text="Search Team:")
        search_label.pack(padx=5, pady=5, anchor="w")
        self.search_entry = ttk.Entry(self.team_tab)
        self.search_entry.pack(fill="x", padx=5)

        ttk.Button(self.team_tab, text="Search", command=self.search_team).pack(pady=5)
        ttk.Button(self.team_tab, text="Load Teams", command=self.load_teams).pack(pady=5)
        ttk.Button(self.team_tab, text="Edit Selected Team", command=lambda: self.edit_item(self.team_table, "Teams")).pack(pady=5)
        ttk.Button(self.team_tab, text="Delete Selected Team", command=self.delete_team).pack(pady=5)

    def create_player_tab(self):
        columns = ("ID", "Full Name", "Jersey Number", "Team ID")
        self.player_table = ttk.Treeview(self.player_tab, columns=columns, show="headings")
        for col in columns:
            self.player_table.heading(col, text=col)
        self.player_table.pack(fill="both", expand=True)

        # Поля поиска и кнопки
        search_label = ttk.Label(self.player_tab, text="Search Player:")
        search_label.pack(padx=5, pady=5, anchor="w")
        self.player_search_entry = ttk.Entry(self.player_tab)
        self.player_search_entry.pack(fill="x", padx=5)

        ttk.Button(self.player_tab, text="Search", command=self.search_player).pack(pady=5)
        ttk.Button(self.player_tab, text="Load Players", command=self.load_players).pack(pady=5)
        ttk.Button(self.player_tab, text="Edit Selected Player", command=lambda: self.edit_item(self.player_table, "Players")).pack(pady=5)
        ttk.Button(self.player_tab, text="Delete Selected Player", command=self.delete_player).pack(pady=5)

    def create_stadium_tab(self):
        columns = ("ID", "Name", "City", "Capacity")
        self.stadium_table = ttk.Treeview(self.stadium_tab, columns=columns, show="headings")
        for col in columns:
            self.stadium_table.heading(col, text=col)
        self.stadium_table.pack(fill="both", expand=True)

        # Поля поиска и кнопки
        search_label = ttk.Label(self.stadium_tab, text="Search Stadium:")
        search_label.pack(padx=5, pady=5, anchor="w")
        self.stadium_search_entry = ttk.Entry(self.stadium_tab)
        self.stadium_search_entry.pack(fill="x", padx=5)

        ttk.Button(self.stadium_tab, text="Search", command=self.search_stadium).pack(pady=5)
        ttk.Button(self.stadium_tab, text="Load Stadiums", command=self.load_stadiums).pack(pady=5)
        ttk.Button(self.stadium_tab, text="Edit Selected Stadium", command=lambda: self.edit_item(self.stadium_table, "Stadiums")).pack(pady=5)
        ttk.Button(self.stadium_tab, text="Delete Selected Stadium", command=self.delete_stadium).pack(pady=5)

    def create_match_tab(self):
        columns = ("ID", "Home Team", "Away Team", "Stadium", "Date", "Ticket Price")
        self.match_table = ttk.Treeview(self.match_tab, columns=columns, show="headings")
        for col in columns:
            self.match_table.heading(col, text=col)
        self.match_table.pack(fill="both", expand=True)

        # Поля поиска и кнопки
        search_label = ttk.Label(self.match_tab, text="Search Match:")
        search_label.pack(padx=5, pady=5, anchor="w")
        self.match_search_entry = ttk.Entry(self.match_tab)
        self.match_search_entry.pack(fill="x", padx=5)

        ttk.Button(self.match_tab, text="Search", command=self.search_match).pack(pady=5)
        ttk.Button(self.match_tab, text="Load Matches", command=self.load_matches).pack(pady=5)
        ttk.Button(self.match_tab, text="Edit Selected Match", command=lambda: self.edit_item(self.match_table, "Matches")).pack(pady=5)
        ttk.Button(self.match_tab, text="Delete Selected Match", command=self.delete_match).pack(pady=5)

    def create_performance_tab(self):
        columns = ("Match ID", "Player ID", "Goals")
        self.performance_table = ttk.Treeview(self.performance_tab, columns=columns, show="headings")
        for col in columns:
            self.performance_table.heading(col, text=col)
        self.performance_table.pack(fill="both", expand=True)

        # Поля поиска и кнопки
        search_label = ttk.Label(self.performance_tab, text="Search Performance:")
        search_label.pack(padx=5, pady=5, anchor="w")
        self.performance_search_entry = ttk.Entry(self.performance_tab)
        self.performance_search_entry.pack(fill="x", padx=5)

        ttk.Button(self.performance_tab, text="Search", command=self.search_performance).pack(pady=5)
        ttk.Button(self.performance_tab, text="Load Performance", command=self.load_performance).pack(pady=5)
        ttk.Button(self.performance_tab, text="Edit Selected Performance", command=lambda: self.edit_item(self.performance_table, "Performance")).pack(pady=5)
        ttk.Button(self.performance_tab, text="Delete Selected Performance", command=self.delete_performance).pack(pady=5)

    def edit_item(self, table, table_name):
        # Получаем выбранный элемент
        selected_item = table.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an item to edit.")
            return

        values = table.item(selected_item, "values")

        # Создаем окно редактирования
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Entry")
        edit_window.geometry("400x300")

        # Создаем поля ввода
        labels = []
        entries = []
        columns = self.db.get_table_columns(table_name)

        for i, col in enumerate(columns):
            lbl = ttk.Label(edit_window, text=col)
            lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = ttk.Entry(edit_window)
            entry.insert(0, values[i])  # Заполняем текущими значениями
            entry.grid(row=i, column=1, padx=10, pady=5)
            labels.append(lbl)
            entries.append(entry)

        def save_changes():
            # Получаем новые значения
            new_values = [entry.get() for entry in entries]

            # Обновляем запись в базе данных
            update_query = f"UPDATE {table_name} SET "
            update_query += ", ".join([f"{col} = ?" for col in columns[1:]])  # Пропускаем ID
            update_query += f" WHERE {columns[0]} = ?"

            self.db.update_data(update_query, new_values[1:] + [new_values[0]])

            # Обновляем запись в таблице UI
            table.item(selected_item, values=new_values)
            messagebox.showinfo("Success", "Data updated successfully!")
            edit_window.destroy()

        ttk.Button(edit_window, text="Save", command=save_changes).grid(row=len(columns), columnspan=2, pady=10)
