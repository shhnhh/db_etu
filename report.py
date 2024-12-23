import tkinter as tk
from tkinter import ttk, messagebox


# Main application class
class ReportData(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app)

        self.db = app.db

        self.title("Stadium Report Generator")
        self.geometry("1000x600")

        # Create Widgets
        self.create_widgets()

    def create_widgets(self):
        # Input for stadium name
        tk.Label(self, text="Stadium Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.stadium_name_entry = tk.Entry(self)
        self.stadium_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Fetch Report Button
        self.fetch_button = tk.Button(self, text="Fetch Report", command=self.fetch_report)
        self.fetch_button.grid(row=0, column=2, padx=10, pady=5)

        # Report TreeView
        columns = ("Total Matches", "Home Wins", "Guest Wins", "Scorer", "Stadium Name")
        self.report_tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.report_tree.heading(col, text=col)
        self.report_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Configure column weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def fetch_report(self):
        stadium_name = self.stadium_name_entry.get().strip()
        if not stadium_name:
            messagebox.showwarning("Input Error", "Please enter a stadium name.")
            return

        # Fetch data from database
        stadium_id = self.db.get_id_by_name('Stadiums', 'name', stadium_name)
        report_data = self.db.generate_stadium_report(stadium_id)
        if not report_data:
            messagebox.showinfo("No Data", "No matches found for the specified stadium.")
            return

        # Clear previous entries in the TreeView
        for row in self.report_tree.get_children():
            self.report_tree.delete(row)

        # Populate TreeView with new data
        self.report_tree.insert("", "end", values=report_data)