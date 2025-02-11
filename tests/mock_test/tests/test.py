import unittest

class Test(unittest.TestCase):

    '''
    This test (and the whole sub-package called "test_run_tests_package") is used to check if the function run_tests work 
    as intended by running the tests
    '''
    def test(self):
        self.assertFalse(True)
if __name__ == '__main__':
    unittest.main()