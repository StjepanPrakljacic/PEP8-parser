import os
import sys
import time
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


def main():
    """
    The main function to be executed.
    Args:
        None
    Returns:
        None
    """
    folder_path = os.path.normpath(get_folder_path())
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Path not found: {folder_path}")
    try:
        with FolderHandler(folder_path) as folder_contents:
            if len(folder_contents) == 0:
                raise FolderHandlerError(
                f"No Python files were found at: {folder_path}")
            for path in folder_contents:
                file_handler = FileHandler(path)
                pycodestyle_output = file_handler.run_pycodestyle()
                if not isinstance(pycodestyle_output, str):
                    raise TypeError("Type error for pycodestyle output.")
                style_violations = file_handler.parse_pycodestyle_output(
                    pycodestyle_output)
                for violation in style_violations:
                    log_obj.info(violation)
                time.sleep(1)
    except FolderHandlerError as folder_error:
        log_obj.error(folder_error)
    except Exception as e:
        log_obj.error(e)
        sys.exit(1)
    return True

if __name__ == "__main__":
    main()