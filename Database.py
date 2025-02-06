import sqlite3

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS builds (
                id TEXT PRIMARY KEY,
                commit_id TEXT,
                timestamp TEXT,
                log TEXT
            )
        """)
        conn.commit()
        conn.close()

    def execute(self, query, params=()):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute(query, params)
        result = c.fetchall()
        conn.commit()
        conn.close()
        return result
