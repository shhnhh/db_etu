import sqlite3

class DataBase:

    def __init__(self):
        # Database connection
        self.conn = sqlite3.connect("football.db")
        self.cursor = self.conn.cursor()

        # Create tables
        self.cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            coach_name TEXT NOT NULL,
            last_season_rank INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            jersey_number INTEGER NOT NULL,
            team_id INTEGER,
            FOREIGN KEY (team_id) REFERENCES Teams (id)
        );

        CREATE TABLE IF NOT EXISTS Stadiums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            capacity INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            home_team_id INTEGER NOT NULL,
            away_team_id INTEGER NOT NULL,
            stadium_id INTEGER NOT NULL,
            date DATE NOT NULL,
            home_team_score INTEGER NOT NULL,
            away_team_score INTEGER NOT NULL,
            ticket_price REAL NOT NULL,
            FOREIGN KEY (home_team_id) REFERENCES Teams (id),
            FOREIGN KEY (away_team_id) REFERENCES Teams (id),
            FOREIGN KEY (stadium_id) REFERENCES Stadiums (id)
        );

        CREATE TABLE IF NOT EXISTS Performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            goals INTEGER NOT NULL,
            FOREIGN KEY (match_id) REFERENCES Matches (id),
            FOREIGN KEY (player_id) REFERENCES Players (id)
        );
        ''')

        self.conn.commit()

    # Function definitions
    def add_team(self, name, city, coach_name, last_season_rank):
        self.cursor.execute("INSERT INTO Teams (name, city, coach_name, last_season_rank) VALUES (?, ?, ?, ?)",
                    (name, city, coach_name, last_season_rank))
        self.conn.commit()

    def add_player(self, full_name, jersey_number, team_id):
        self.cursor.execute("INSERT INTO Players (full_name, jersey_number, team_id) VALUES (?, ?, ?)",
                    (full_name, jersey_number, team_id))
        self.conn.commit()

    def add_stadium(self, name, city, capacity):
        self.cursor.execute("INSERT INTO Stadiums (name, city, capacity) VALUES (?, ?, ?)", (name, city, capacity))
        self.conn.commit()

    def add_match(self, home_team_id, away_team_id, stadium_id, date, ticket_price):
        self.cursor.execute("INSERT INTO Matches (home_team_id, away_team_id, stadium_id, date, ticket_price, home_team_score, away_team_score) VALUES (?, ?, ?, ?, ?, 0, 0)",
                    (home_team_id, away_team_id, stadium_id, date, ticket_price))
        self.conn.commit()

    def record_performance(self, match_id, player_id, goals):
        self.cursor.execute("INSERT INTO Performance (match_id, player_id, goals) VALUES (?, ?, ?)",
                    (match_id, player_id, goals))
        
        self.cursor.execute('''
            UPDATE Matches
            SET 
                home_team_score = (CASE WHEN home_team_id = (SELECT team_id FROM Players WHERE id = ?) 
                                        THEN home_team_score + ? ELSE home_team_score END),
                away_team_score = (CASE WHEN away_team_id = (SELECT team_id FROM Players WHERE id = ?) 
                                        THEN away_team_score + ? ELSE away_team_score END)
            WHERE id = ?''', 
            (player_id, goals, player_id, goals, match_id)
        )
        
        self.conn.commit()

    def update_player_team(self, player_id, new_team_id):
        self.cursor.execute("UPDATE Players SET team_id = ? WHERE id = ?", (new_team_id, player_id))
        self.conn.commit()

    def cancel_match(self, match_id):
        self.cursor.execute("DELETE FROM Matches WHERE id = ?", (match_id,))
        self.conn.commit()

    def change_coach(self, team_id, new_coach_name):
        self.cursor.execute("UPDATE Teams SET coach_name = ? WHERE id = ?", (new_coach_name, team_id))
        self.conn.commit()

    def get_team_matches(self, team_id):
        self.cursor.execute('''
            SELECT m.date, t1.name AS opponent, m.home_team_score, m.away_team_score, s.name AS stadium
            FROM Matches m
            JOIN Teams t1 ON (m.home_team_id = t1.id OR m.away_team_id = t1.id)
            JOIN Stadiums s ON m.stadium_id = s.id
            WHERE m.home_team_id = ? OR m.away_team_id = ?''', (team_id, team_id))
        return self.cursor.fetchall()

    def get_player_performance(self, team_id, date, player_name):
        self.cursor.execute('''
            SELECT p.full_name, p.jersey_number, perf.goals
            FROM Players p
            JOIN Performance perf ON p.id = perf.player_id
            JOIN Matches m ON perf.match_id = m.id
            WHERE m.date = ? AND p.team_id = ? AND p.full_name = ?''', (date, team_id, player_name))
        return self.cursor.fetchone()

    def get_ticket_price(self, home_team_id, away_team_id):
        self.cursor.execute('''
            SELECT m.ticket_price
            FROM Matches m
            WHERE m.home_team_id = ? AND m.away_team_id = ?''', (home_team_id, away_team_id))
        return self.cursor.fetchone()

    def generate_stadium_report(self, stadium_id):
        # Сначала получим общее количество матчей и побед
        self.cursor.execute('''
            SELECT 
                COUNT(m.id) AS total_matches, 
                SUM(CASE WHEN m.home_team_score > m.away_team_score THEN 1 ELSE 0 END) AS home_wins,
                SUM(CASE WHEN m.home_team_score < m.away_team_score THEN 1 ELSE 0 END) AS away_wins,
                s.name AS stadium_name
            FROM Matches m
            JOIN Stadiums s ON m.stadium_id = s.id
            WHERE s.id = ?
            GROUP BY s.id;
        ''', (stadium_id,))
        stadium_data = self.cursor.fetchone()

        # Если данных о стадионе нет, возвращаем None
        if not stadium_data:
            return None

        total_matches, home_wins, away_wins, stadium_name = stadium_data

        # Затем находим самого результативного игрока
        self.cursor.execute('''
            SELECT 
                p.full_name, 
                SUM(perf.goals) AS total_goals
            FROM Performance perf
            JOIN Players p ON perf.player_id = p.id
            JOIN Matches m ON m.id = perf.match_id
            WHERE m.stadium_id = ?
            GROUP BY p.id
            ORDER BY total_goals DESC
            LIMIT 1;
        ''', (stadium_id,))
        top_scorer = self.cursor.fetchone()

        # Имя самого результативного игрока (если есть)
        top_scorer_name = top_scorer[0] if top_scorer else None

        return total_matches, home_wins, away_wins, top_scorer_name, stadium_name

    # Cleanup
    def close_connection(self):
        self.conn.close()

    def fetch_data(self, query, args=[]):
        self.cursor.execute(query, args)
        return self.cursor.fetchall()
    
    def delete_team(self, team_id):
        query = "DELETE FROM Teams WHERE id = ?"
        self.cursor.execute(query, (team_id,))
        self.conn.commit()

    # Функция для удаления игрока
    def delete_player(self, player_id):
        query = "DELETE FROM Players WHERE id = ?"
        self.cursor.execute(query, (player_id,))
        self.conn.commit()

    # Функция для удаления стадиона
    def delete_stadium(self, stadium_id):
        query = "DELETE FROM Stadiums WHERE id = ?"
        self.cursor.execute(query, (stadium_id,))
        self.conn.commit()

    # Функция для удаления матча
    def delete_match(self, match_id):
        query = "DELETE FROM Matches WHERE id = ?"
        self.cursor.execute(query, (match_id,))
        self.conn.commit()

    # Функция для удаления записи о производительности игрока
    def delete_performance(self, performance_id):
        query = "DELETE FROM Performance WHERE match_id = ?"
        self.cursor.execute(query, (performance_id,))
        self.conn.commit()

    def update_data(self, query, parameters):
        self.cursor.execute(query, parameters)
        self.conn.commit()

    def get_table_columns(self, table_name):
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        return [row[1] for row in self.cursor.fetchall()]
    
    def get_id_by_name(self, table_name, name_column, name_value):
        self.cursor.execute(f"SELECT id FROM {table_name} WHERE {name_column} = ?", (name_value,))
        result = self.cursor.fetchone()  # Возвращает первую строку результата
        return result[0] if result else None