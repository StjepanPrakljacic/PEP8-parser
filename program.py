# PyCode Style Checker - Automated Correction

# Description: A Python script that automates the checking and correction of
#              style violations in Python code files within a specified folder.
#              It utilizes the PyCode Style Corrective module to address issues
#              such as import positioning, multiple imports on one line,
#              and blank line spacing within classes and functions.

# Created by: Stjepan Prakljačić
# License: MIT License, all rights reserved.
# Repository: https://github.com/StjepanPrakljacic/PEP8-parser.git

# Version: 1.0.0
###############################################################################

import os
import sys
from tkinter import Tk, filedialog
from Scripts.folder_handler import FolderHandler
from Scripts.logging_handler import log_obj
from Scripts.file_handler import FileHandler
from Scripts.error_handler import *


def get_folder_path():
    """
    Opens a GUI for the user to select a folder and returns the selected path.
    Returns:
        str: The selected folder path.
    """
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    return folder_path


def ask_user_open_file(file_path):
    """
    Asks the user if they would like to open the file in a code editor.
    Args:
        file_path (str): The path of the file to be opened.
    Returns:
        bool: True if the user chooses to open the file, False otherwise.
    """
    file_name = os.path.basename(file_path)
    while True:
        log_obj.info(f"Do you want to open '{file_name}' in a code editor?" \
                     "(y/n): ")
        user_input = input().lower()

        if user_input in ('y', 'n'):
            if user_input == 'y':
                return True
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def main():
    """
    The main function to be executed.
    Args:
        None
    Returns:
        None
    """
    try:
        folder_path = os.path.normpath(get_folder_path())

        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Path not found: {folder_path}")

        with FolderHandler(folder_path) as folder_contents:
            if len(folder_contents) == 0:
                raise FolderHandlerError(
                    f"No Python files were found at: {folder_path}"
                    )
            for path in folder_contents:
                file_handler = FileHandler(path)
                file_handler.run_pycodestyle()
                if ask_user_open_file(path):
                    file_handler.open()

    except FileNotFoundError as file_not_found_error:
        log_obj.error(file_not_found_error)
        sys.exit(1)
    except FolderHandlerError as folder_error:
        log_obj.error(folder_error)
    except Exception as e:
        log_obj.error(e)
    return True


if __name__ == "__main__":
    main()
