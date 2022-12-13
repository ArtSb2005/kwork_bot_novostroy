import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def add_user(self, user_id, username, status):
        with self.conn:
            self.cursor.execute("""INSERT INTO users (user_id, username, 
                    status) VALUES (?, ?, ?)""",
                                (user_id, username, status))

    def update_status(self, user_id, status, phone):
        with self.conn:
            return self.cursor.execute("UPDATE users SET status = ?, phone = ? WHERE user_id = ?",
                                       (status, phone, user_id,))

    def get_users(self):
        with self.conn:
            result = self.cursor.execute("SELECT user_id, status FROM users").fetchall()
            return result

    def get_all_users(self):
        with self.conn:
            result = self.cursor.execute("SELECT user_id, username, status, phone FROM users").fetchall()
            return result