import sqlite3

class Database:
    """
    A class to represent a database connection and operations.

    Attributes
    ----------
    db_file : str
        The path to the SQLite database file.

    Methods
    -------
    __init__(db_file):
        Initializes the database connection and creates the builds table if it does not exist.
    
    init_db():
        Creates the builds table if it does not exist.
    
    fetch(query, params=()):
        Fetches results from the database without modifying it.
    
    execute(query, params=()):
        Executes a query that modifies the database.
    """
    def __init__(self, db_file):
        """
        Initializes the Database object.
        Args:
            db_file (str): The path to the database file.
        """
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        """
        Initializes the database by creating the 'builds' table if it does not already exist.
        The 'builds' table contains the following columns:
        - id: TEXT, primary key
        - commit_id: TEXT, the ID of the commit
        - timestamp: TEXT, the timestamp of the build
        - log: TEXT, the log of the build
        This method uses a context manager to connect to the SQLite database specified by self.db_file.
        """
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
        """
        Fetch results from the database without modifying it.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): The parameters to bind to the query. Defaults to ().

        Returns:
            list: A list of tuples containing the fetched rows.
        """
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()
            c.execute(query, params)
            return c.fetchall()

    def execute(self, query, params=()):
        """
        Execute a query that modifies the database.
        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): The parameters to be used with the SQL query. Defaults to ().
        Raises:
            sqlite3.DatabaseError: If an error occurs while executing the query.
        """
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()
            c.execute(query, params)
            conn.commit()
