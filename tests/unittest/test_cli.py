import unittest
import subprocess
import sys
from rickle.tools import classify_string
import os

os.putenv('COMSPEC',r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe')

class TestCLITool(unittest.TestCase):

    def setUp(self) -> None:
        self.cat_command = 'type' if sys.platform == 'win32' else 'cat'
        self.path_sep = '\\' if sys.platform == 'win32' else '/'
        self.placebos_path = r'.\tests\placebos' if sys.platform == 'win32' else './tests/placebos'

        self.python_command = 'python'
        self.rickled_command = 'rickle.cli'

        self.conv_tool = 'conv'
        self.obj_tool = 'obj'
        self.obj_tool_get = 'get'
        self.schema_tool = 'schema'
        self.schema_tool_check = 'check'
        self.schema_tool_gen = 'gen'

    def test_cli_conv(self):

        command_cat = f'{self.cat_command} {self.placebos_path}{self.path_sep}conv_test.json'

        result = subprocess.Popen(command_cat,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)

        command_rickle = f"{self.python_command} -m {self.rickled_command} {self.conv_tool}"

        result = subprocess.run(command_rickle,
                                shell=True,
                                stdin=result.stdout,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)



        # Check if the command was successful
        self.assertEqual(result.returncode, 0, msg=f"CLI returned non-zero exit code: {result.returncode}")

        # Compare actual and expected output
        self.assertEqual(classify_string(result.stdout), 'yaml', msg=f"Unexpected CLI output: {result.stdout}")


if __name__ == "__main__":
    unittest.main()
