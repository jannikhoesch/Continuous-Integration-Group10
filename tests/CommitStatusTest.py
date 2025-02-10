import unittest
import os
from Database import Database
from CommitStatus import send_commit_status

class TestCommitStatus(unittest.TestCase):

    def test_commit_status_success(self):
        commit_SHA = "a284bfc59fd6f157f65b71d027fcf09d8194066c"
        status = "success"
        description = "TESTING THE THING"
        target_url = "http://127.0.0.1:8000"
        result = send_commit_status(commit_SHA, status, description, target_url)
        self.assertEqual(result, True)

    def test_commit_status_fail(self):
        # Incorrect commit SHA
        commit_SHA = "284bfc59fd6f157f65b71d027fcf09d8194066c"
        status = "success"
        description = "TESTING THE THING"
        target_url = "http://127.0.0.1:8000"
        result = send_commit_status(commit_SHA, status, description, target_url)
        self.assertEqual(result, False)

        # Incorrect status value
        commit_SHA = "a284bfc59fd6f157f65b71d027fcf09d8194066c"
        status = "test"
        description = "TESTING THE THING"
        target_url = "http://127.0.0.1:8000"
        result = send_commit_status(commit_SHA, status, description, target_url)
        self.assertEqual(result, False)

if __name__ == '__main__':
    unittest.main()