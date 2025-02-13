import unittest
import os
from src.Database import Database

class TestDatabase(unittest.TestCase):
    """
    Unit tests for the Database class.

    This test suite includes the following tests:

    1. test_init_db: Ensures that the database file is created upon initialization.
    2. test_insert_and_fetch: Ensures that a record can be inserted into the database and then fetched correctly.

    Each test creates a temporary database file named 'test_builds.db' and removes it after the test is completed to ensure isolation between tests.
    """

    def test_init_db(self):
        """
        Test the initialization of the database.

        This test checks if the database file is created successfully when
        initializing a new Database object. It first removes any existing
        database file with the same name, then creates a new Database object
        and verifies that the database file is created. Finally, it removes
        the created database file.

        Steps:
        1. Define the database file name.
        2. Remove the database file if it already exists.
        3. Initialize a new Database object with the defined file name.
        4. Assert that the database file exists.
        5. Remove the created database file.
        """
        db_file = "test_builds.db"
        if os.path.exists(db_file):
            os.remove(db_file)
        db = Database(db_file)
        self.assertTrue(os.path.exists(db_file))
        os.remove(db_file)

    def test_insert_and_fetch(self):
        """
        Test the insertion and fetching of data in the database.

        This test performs the following steps:
        1. Creates a temporary database file named "test_builds.db".
        2. Removes the file if it already exists.
        3. Initializes the Database object with the temporary file.
        4. Inserts a record into the "builds" table.
        5. Fetches the inserted record from the "builds" table.
        6. Asserts that the fetched record matches the inserted data.
        7. Removes the temporary database file after the test.

        The inserted record contains the following fields:
        - id: "1"
        - commit_id: "commit1"
        - timestamp: "2023-01-01T00:00:00"
        - log: "log1"
        """
        db_file = "test_builds.db"
        if os.path.exists(db_file):
            os.remove(db_file)
        db = Database(db_file)
        db.execute("INSERT INTO builds (id, commit_id, timestamp, log) VALUES (?, ?, ?, ?)",
                   ("1", "commit1", "2023-01-01T00:00:00", "log1"))
        result = db.fetch("SELECT * FROM builds WHERE id = ?", ("1",))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "1")
        self.assertEqual(result[0][1], "commit1")
        self.assertEqual(result[0][2], "2023-01-01T00:00:00")
        self.assertEqual(result[0][3], "log1")
        os.remove(db_file)

if __name__ == '__main__':
    unittest.main()