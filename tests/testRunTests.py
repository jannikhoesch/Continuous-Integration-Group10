import unittest
from src.ContinuousIntegrationServer import run_tests

class TestRunTests(unittest.TestCase):
    """
    TestRunTests is a test case class for testing the run_tests function.

    Methods:
        test_run_tests_function: Tests the run_tests function with a mock test directory and a sample commit SHA.
    """

    def test_run_tests_function(self):
        """
        Test the run_tests function.
        This test verifies that the run_tests function correctly identifies
        a failing test case. It uses a mock test directory and a dummy commit
        SHA to simulate the test environment.
        Assertions:
            self.assertFalse(result[0]): Asserts that the first element of the result
            returned by run_tests is False, indicating a test failure.
        """
        
        temp_dir = "tests/mock_test"
        commit_sha = "123"
        result = run_tests(temp_dir, commit_sha)
        self.assertFalse(result[0])

if __name__ == '__main__':
    unittest.main()