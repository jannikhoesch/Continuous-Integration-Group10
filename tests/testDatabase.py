import unittest
import os
from src.Database import Database

class TestDatabase(unittest.TestCase):

    def test_init_db(self):
        """
        Ensures that the database file is created.
        """

        db_file = "test_builds.db"
        if os.path.exists(db_file):
            os.remove(db_file)
        db = Database(db_file)
        self.assertTrue(os.path.exists(db_file))
        os.remove(db_file)

    def test_insert_and_fetch(self):
        """
        Ensures that a record can be inserted and then fetched correctly.
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