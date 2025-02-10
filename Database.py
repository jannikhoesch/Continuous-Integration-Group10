import sqlite3

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_file) as conn:
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

    def fetch(self, query, params=()):
        """Fetch results without modifying the database."""
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()
            c.execute(query, params)
            return c.fetchall()

    def execute(self, query, params=()):
        """Execute a query that modifies the database."""
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()
            c.execute(query, params)
            conn.commit()
