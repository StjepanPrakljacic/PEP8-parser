import os
from tkinter import Tk, filedialog
from Scripts.folder_handler import FolderHandler
from Scripts.logging_handler import log_obj
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
    selected_folder_path = os.path.normpath(get_folder_path())
    with FolderHandler(selected_folder_path) as folder_contents:
        for path in folder_contents:
            log_obj.info(f"Detected and created: {path}")

if __name__ == "__main__":
    main()