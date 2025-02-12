import unittest
import tempfile
import os
from src.ContinuousIntegrationServer import clone_repo

class TestCloneRepo(unittest.TestCase):
    """
    TestCloneRepo is a test case for testing the clone_repo function.

    Methods:
        test_clone_repo(self):
            Tests the clone_repo function by cloning a specific repository, branch, and commit.
            Verifies that the README.md file exists in the cloned repository.
    """
    def test_clone_repo(self):
        """
        Test the clone_repo function.
        This test clones a specific repository from GitHub, checks out a specific branch and commit,
        and verifies that a README.md file exists in the cloned repository.
        Steps:
        1. Define the repository URL, branch, and commit SHA.
        2. Create a temporary directory to clone the repository into.
        3. Call the clone_repo function with the specified parameters.
        4. Assert that the README.md file exists in the cloned repository.
        Raises:
            AssertionError: If the README.md file does not exist in the cloned repository.
        """
        
        repo_url = "https://github.com/amaekh/repo_to_test_CI_server.git"
        branch = "main"
        commit_sha = "7298ed0779eb322f572be61baa793b96e2b579f2"

        with tempfile.TemporaryDirectory() as temp_dir:
            clone_repo(repo_url, branch, commit_sha, temp_dir)
            self.assertTrue(os.path.isfile(f"{temp_dir}/README.md"))

if __name__ == '__main__':
    unittest.main()