import datetime
import sqlite3
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "game_history.db")

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                player_name TEXT, 
                                reaction_time INTEGER, 
                                played_at TEXT,
                                game_mode TEXT,
                                score INTEGER
                                )''')
        self.conn.commit()

    def save_record(self, game_mode, name, r_time, score):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # r_time이 None일 경우 처리
        if r_time is None:
            reaction_ms = None
            final_score = 0
        else:
            reaction_ms = int(r_time * 1000)
            final_score = score

        self.cursor.execute(
            f"""INSERT INTO history
                    (game_mode, player_name, reaction_time, score, played_at)
                VALUES
                    (?, ?, ?, ?, ?)
            """,
            (game_mode, name, reaction_ms, final_score, now)
        )
        self.conn.commit()

    def get_stats_by_player(self, game_mode, player_name):
        self.cursor.execute(
            """SELECT
                DATE(played_at),
                MAX(score),
                AVG(score)
            FROM
                history
            WHERE
                game_mode = ? AND player_name = ?
            GROUP BY
                DATE(played_at)
            ORDER BY
                DATE(played_at) ASC
            """,
            (game_mode, player_name)
        )
        return self.cursor.fetchall()

    def get_all_player_names(self):
        self.cursor.execute(
            """
                SELECT
                    DISTINCT player_name
                FROM
                    history
                ORDER BY
                    player_name ASC
            """
        )
        return [row[0] for row in self.cursor.fetchall()]

    def get_all_stats_for_player(self, player_name):
        stats_by_game = {}
        game_modes = ["GAME1", "GAME2", "GAME3"]

        for mode in game_modes:
            # reaction_time < 9000 to filter out invalid/failed rounds
            self.cursor.execute(
                """SELECT
                    AVG(reaction_time),
                    MIN(reaction_time),
                    COUNT(*),
                    AVG(score)
                FROM
                    history
                WHERE
                    player_name = ? AND game_mode = ? AND reaction_time < 9000
                """,
                (player_name, mode)
            )
            result = self.cursor.fetchone()
            if result and result[0] is not None:
                stats_by_game[mode] = {
                    'avg_r_time': result[0],
                    'best_r_time': result[1],
                    'total_rounds': result[2],
                    'avg_score': result[3]
                }

        return {
            "player_name": player_name,
            "games": stats_by_game
        }

    def close(self):
        self.conn.close();
