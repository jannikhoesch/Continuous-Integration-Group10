import unittest
import tempfile
import os
from src.ContinuousIntegrationServer import compile_project

class TestCompileProject(unittest.TestCase):
    """
    Unit tests for the compile_project function.

    Methods:
    - test_compile_project_success: Tests that the compile_project function successfully compiles a valid Python project.
    - test_compile_project_failure: Tests that the compile_project function fails to compile an invalid Python project.
    """

    def test_compile_project_success(self):
        """
        Test case for successfully compiling a project.

        This test creates a temporary directory and writes a valid Python script
        into it. It then calls the compile_project function to compile the script
        and asserts that the compilation is successful.

        The test performs the following steps:
        1. Creates a temporary directory.
        2. Writes a valid Python script ("print('Hello, World!')") into the directory.
        3. Calls the compile_project function with the temporary directory as an argument.
        4. Asserts that the compile_project function returns success.

        This ensures that the compile_project function can correctly compile a valid
        Python script.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a valid Python file
            with open(os.path.join(temp_dir, "valid_script.py"), "w") as f:
                f.write("print('Hello, World!')")

            success, log = compile_project(temp_dir)
            self.assertTrue(success)

    def test_compile_project_failure(self):
        """
        Test case for compile_project function to check failure scenario.

        This test creates a temporary directory and writes an invalid Python script
        into it. It then calls the compile_project function with the directory
        containing the invalid script and asserts that the compilation fails.

        The invalid script contains a syntax error to ensure the compilation fails.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create an invalid Python file
            with open(os.path.join(temp_dir, "invalid_script.py"), "w") as f:
                f.write("print('Hello, World!'\n")

            success, log = compile_project(temp_dir)
            self.assertFalse(success)

if __name__ == '__main__':
    unittest.main()
