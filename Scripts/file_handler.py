import os
import subprocess
import re
from .logging_handler import log_obj

class FileHandler():
    """
    A class representing a handler for managing Python files.

    Attributes:
        file_path (str): The path to the Python file to be handled.

    Methods:
        __init__(self, file_path):
            Initialize the FileHandler instance.

        run_pycodestyle(self):
            Run Pycodestyle on the specified Python file and return the output.

        parse_pycodestyle_output(self, output):
            Parse the Pycodestyle output to extract style violations.

        open(self):
            Open the specified Python file in the default editor.

    Usage:
        file_handler = FileHandler("/path/to/file.py")
        pycodestyle_output = file_handler.run_pycodestyle()
        style_violations = file_handler.parse_pycodestyle_output(pycodestyle_output)
        file_handler.open()
    """
    def __init__(self, file_path):
        if os.path.exists(file_path):
            self.file_path = file_path
        else:
            raise FileNotFoundError(f"Path not found: {file_path}")


    def run_pycodestyle(self):
        log_obj.info(f"Opening file at: {self.file_path}")
        result = subprocess.run(['pycodestyle', self.file_path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        return result.stdout


    def parse_pycodestyle_output(self, output):
        violations = []
        for line in output.splitlines():
            match = re.match(r'^(.*):(\d+):(\d+): (.+)$', line)
            if match:
                file_path, line_number, column_number, violation_type =(
                    match.groups()
                 )
                violations.append({
                    'file_path': file_path,
                    'line_number': int(line_number),
                    'column_number': int(column_number),
                    'violation_type': violation_type
                })
        return violations


    def open(self):
        subprocess.Popen(['code', self.file_path], shell=True)
