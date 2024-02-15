# PyCode Style file handler module

# Description: A class representing a handler for managing Python files.
#              Designed to automatically correct style violations in Python
#              code files.

# Created by: Stjepan Prakljačić
# License: MIT License, all rights reserved.
# Repository: https://github.com/StjepanPrakljacic/PEP8-parser.git
#
# Version: 1.0.0
###############################################################################

import sys
import subprocess
import time
from .logging_handler import log_obj
from .violations import *
from .corrective_actions import *


class FileHandler():
    """
    A class representing a handler for managing Python files.

    Attributes:
        file_path (str): The path to the Python file to be handled.

    Methods:
        __init__(self, file_path):
            Initializes the FileHandler instance.

        run_pycodestyle(self):
            Runs code style analysis on the specified Python file and applies
            corrective actions to fix style violations.

        parse_pycodestyle_output(self, output):
            Parses the Pycodestyle output to extract style violations.

        read_from_file(self):
            Reads the content of the specified Python file.

        analyze(self, callback_check, callback_fix):
            Analyzes the Python file for style violations using the specified
            check and fix callbacks.

        open(self):
            Opens the specified Python file in the default code editor.

    Usage:
        file_handler = FileHandler("/path/to/file.py")
        file_handler.run_pycodestyle()
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def read_from_file(self):
        """
        Reads the content of the specified Python file.

        Returns:
            list: A list containing lines of the file content.
        """
        with open(self.file_path, 'r') as f:
            file_content = f.readlines()
        return file_content

    def analyze(self, callback_check, callback_fix):
        """
        Analyzes the Python file for style violations using the specified
        check and fix callbacks.

        Args:
            callback_check (function): The function to check for style
                                       violations.
            callback_fix (function): The function to fix style violations.
        """
        status = True
        while status:
            file_content = self.read_from_file()
            violations = callback_check(file_content)
            status = self.parse_pycodestyle_output(violations)
            if status:
                callback_fix(self.file_path, file_content, violations)
                #status = False


    def run_pycodestyle(self):
        """
        Runs code style analysis on the specified Python file and applies
        corrective actions to fix style violations.
        """
        log_obj.info(f"Running code style analysis on file: {self.file_path}")
        time.sleep(1)
        self.analyze(extraneous_whitespace_check,
                     extraneous_whitespace_corrective_action)
        time.sleep(1)
        self.analyze(imports_position_check,
                     imports_position_corrective_action)
        time.sleep(1)
        self.analyze(multiple_imports_check,
                     multiple_imports_corrective_action)
        time.sleep(1)
        self.analyze(expected_blank_lines_check,
                     blank_lines_corrective_action)

    def parse_pycodestyle_output(self, output):
        """
        Parses the Pycodestyle output to extract style violations.

        Args:
            output (list): List of style violations.

        Returns:
            bool: True if violations are found, False otherwise.
        """
        if output is not None:
            try:
                if not isinstance(output, list):
                    raise TypeError(
                        f"Expected a list as the output, {type(output)}"
                    )
                for violation in output:
                    log_obj.warning(f"Violation detected: {violation}")
                return True
            except TypeError as type_error:
                log_obj.error(type_error)
                sys.exit(1)
        return False

    def open(self):
        """
        Opens the specified Python file in the default code editor.
        """
        log_obj.info(f"Opening file in code editor: {self.file_path}")
        time.sleep(1)
        subprocess.Popen(['code', self.file_path], shell=True)
