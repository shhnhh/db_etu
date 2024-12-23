import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Main application window
class AddData(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app)

        self.db = app.db

        self.title("Football Team Manager")
        self.geometry("800x600")
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)

        # Tabs
        self.add_team_tab = ttk.Frame(self.tabs)
        self.add_player_tab = ttk.Frame(self.tabs)
        self.add_stadium_tab = ttk.Frame(self.tabs)
        self.add_match_tab = ttk.Frame(self.tabs)
        self.record_performance_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.add_team_tab, text="Add Team")
        self.tabs.add(self.add_player_tab, text="Add Player")
        self.tabs.add(self.add_stadium_tab, text="Add Stadium")
        self.tabs.add(self.add_match_tab, text="Add Match")
        self.tabs.add(self.record_performance_tab, text="Record Performance")

        self.create_add_team_tab()
        self.create_add_player_tab()
        self.create_add_stadium_tab()
        self.create_add_match_tab()
        self.create_record_performance_tab()

    def create_add_team_tab(self):
        tk.Label(self.add_team_tab, text="Team Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.team_name_entry = tk.Entry(self.add_team_tab)
        self.team_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.add_team_tab, text="City:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.city_entry = tk.Entry(self.add_team_tab)
        self.city_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.add_team_tab, text="Coach Name:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.coach_name_entry = tk.Entry(self.add_team_tab)
        self.coach_name_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.add_team_tab, text="Last Season Rank:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.last_season_rank_entry = tk.Entry(self.add_team_tab)
        self.last_season_rank_entry.grid(row=3, column=1, padx=10, pady=5)

        self.add_team_button = tk.Button(self.add_team_tab, text="Add Team", command=self.add_team)
        self.add_team_button.grid(row=4, column=0, columnspan=2, pady=10)

    def add_team(self):
        name = self.team_name_entry.get()
        city = self.city_entry.get()
        coach_name = self.coach_name_entry.get()
        try:
            last_season_rank = int(self.last_season_rank_entry.get())
            self.db.add_team(name, city, coach_name, last_season_rank)
        except ValueError:
            messagebox.showerror("Input Error", "Last Season Rank must be an integer!")

    def create_add_player_tab(self):
        tk.Label(self.add_player_tab, text="Full Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.player_name_entry = tk.Entry(self.add_player_tab)
        self.player_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.add_player_tab, text="Jersey Number:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.jersey_number_entry = tk.Entry(self.add_player_tab)
        self.jersey_number_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.add_player_tab, text="Team ID:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.team_id_entry = tk.Entry(self.add_player_tab)
        self.team_id_entry.grid(row=2, column=1, padx=10, pady=5)

        self.add_player_button = tk.Button(self.add_player_tab, text="Add Player", command=self.add_player)
        self.add_player_button.grid(row=3, column=0, columnspan=2, pady=10)

    def add_player(self):
        full_name = self.player_name_entry.get()
        try:
            jersey_number = int(self.jersey_number_entry.get())
            team_id = int(self.team_id_entry.get())
            self.db.add_player(full_name, jersey_number, team_id)
        except ValueError:
            messagebox.showerror("Input Error", "Jersey Number and Team ID must be integers!")

    def create_add_stadium_tab(self):
        tk.Label(self.add_stadium_tab, text="Stadium Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.stadium_name_entry = tk.Entry(self.add_stadium_tab)
        self.stadium_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.add_stadium_tab, text="City:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.stadium_city_entry = tk.Entry(self.add_stadium_tab)
        self.stadium_city_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.add_stadium_tab, text="Capacity:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.stadium_capacity_entry = tk.Entry(self.add_stadium_tab)
        self.stadium_capacity_entry.grid(row=2, column=1, padx=10, pady=5)

        self.add_stadium_button = tk.Button(self.add_stadium_tab, text="Add Stadium", command=self.add_stadium)
        self.add_stadium_button.grid(row=3, column=0, columnspan=2, pady=10)

    def add_stadium(self):
        name = self.stadium_name_entry.get()
        city = self.stadium_city_entry.get()
        try:
            capacity = int(self.stadium_capacity_entry.get())
            self.db.add_stadium(name, city, capacity)
        except ValueError:
            messagebox.showerror("Input Error", "Capacity must be an integer!")

    def create_add_match_tab(self):
        tk.Label(self.add_match_tab, text="Home Team ID:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.home_team_entry = tk.Entry(self.add_match_tab)
        self.home_team_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.add_match_tab, text="Away Team ID:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.away_team_entry = tk.Entry(self.add_match_tab)
        self.away_team_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.add_match_tab, text="Stadium ID:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.stadium_entry = tk.Entry(self.add_match_tab)
        self.stadium_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.add_match_tab, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.match_date_entry = tk.Entry(self.add_match_tab)
        self.match_date_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.add_match_tab, text="Ticket Price:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.ticket_price_entry = tk.Entry(self.add_match_tab)
        self.ticket_price_entry.grid(row=4, column=1, padx=10, pady=5)

        self.add_match_button = tk.Button(self.add_match_tab, text="Add Match", command=self.add_match)
        self.add_match_button.grid(row=5, column=0, columnspan=2, pady=10)

    def add_match(self):
        try:
            home_team_id = int(self.home_team_entry.get())
            away_team_id = int(self.away_team_entry.get())
            stadium_id = int(self.stadium_entry.get())
            date = self.match_date_entry.get()
            ticket_price = float(self.ticket_price_entry.get())
            self.db.add_match(home_team_id, away_team_id, stadium_id, date, ticket_price)
        except ValueError:
            messagebox.showerror("Input Error", "Ensure IDs and Ticket Price are numeric and date is valid!")

    def create_record_performance_tab(self):
        tk.Label(self.record_performance_tab, text="Match ID:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.match_id_entry = tk.Entry(self.record_performance_tab)
        self.match_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.record_performance_tab, text="Player ID:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.player_id_entry = tk.Entry(self.record_performance_tab)
        self.player_id_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.record_performance_tab, text="Goals:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.goals_entry = tk.Entry(self.record_performance_tab)
        self.goals_entry.grid(row=2, column=1, padx=10, pady=5)

        self.record_performance_button = tk.Button(self.record_performance_tab, text="Record Performance", command=self.record_performance)
        self.record_performance_button.grid(row=3, column=0, columnspan=2, pady=10)

    def record_performance(self):
        try:
            match_id = int(self.match_id_entry.get())
            player_id = int(self.player_id_entry.get())
            goals = int(self.goals_entry.get())
            self.db.record_performance(match_id, player_id, goals)
        except ValueError:
            messagebox.showerror("Input Error", "Match ID, Player ID, and Goals must be integers!")


