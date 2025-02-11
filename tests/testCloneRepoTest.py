import unittest
import tempfile
import os
from src.ContinuousIntegrationServer import clone_repo

class TestCloneRepo(unittest.TestCase):

    def test_clone_repo(self):
        repo_url = "https://github.com/amaekh/repo_to_test_CI_server.git"
        branch = "main"
        commit_sha = "7298ed0779eb322f572be61baa793b96e2b579f2"

        with tempfile.TemporaryDirectory() as temp_dir:
            clone_repo(repo_url, branch, commit_sha, temp_dir)
            self.assertTrue(os.path.isfile(f"{temp_dir}/README.md"))

if __name__ == '__main__':
    unittest.main()