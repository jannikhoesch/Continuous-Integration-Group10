import unittest
from src.ContinuousIntegrationServer import run_tests

class TestRunTests(unittest.TestCase):

    '''
    This test verifies that the run_tests function operates as intended by running unit tests within a specified directory.
    For this purpose, the mock directory mock_test is used to simulate a directory containing unit tests to be executed.
    '''
    def test_run_tests_function(self):
        temp_dir = "tests/mock_test"
        commit_sha = "123"
        result = run_tests(temp_dir, commit_sha)
        self.assertFalse(result[0])

if __name__ == '__main__':
    unittest.main()