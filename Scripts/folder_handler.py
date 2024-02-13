# PyCode Style folder handler module

# Description: A context manager for managing folders and performing actions
#              related to PyCode style corrections.


# Created by: Stjepan Prakljačić
# License: MIT License, all rights reserved.
# Repository: https://github.com/StjepanPrakljacic/PEP8-parser.git
#
# Version: 1.0.0
###############################################################################

import os
import shutil
from .logging_handler import log_obj

class FolderHandler:
    """
    A class representing a context manager for managing a folder.

    Attributes:
        folder_path (str): The path to the folder to be managed..

    Methods:
        __init__(self, folder_path):
            Initialize the FolderHandler instance.

        __enter__(self):
            Enter the managed folder context.

        __exit__(self, exc_type, exc_value, traceback):
            Exit the managed folder context.

    Usage:
        with FolderHandler("/path/to/folder") as folder_contents:
            # Code within the managed folder context.
            # The 'folder_contents' variable holds a list of contents in the
              folder.
        # The folder context has been exited.
    """

    def __init__(self, folder_path):
        if os.path.exists(folder_path):
            self.folder_path = folder_path
        else:
            raise FileNotFoundError(f"Path not found: {folder_path}")

    def __enter__(self):
        log_obj.info(f"Entering folder: {self.folder_path}")
        copied_files = list()
        for folder, sub_folders, file_names in os.walk(self.folder_path):
            for file in file_names:
                original_path = os.path.join(folder, file)
                if all([file.endswith(".py"), "-Copy" not in file]):
                    file = os.path.splitext(file)[0]
                    file = f"{file}-Copy.py"
                    copy_path = os.path.join(folder, file)
                    shutil.copy2(original_path, copy_path)
                    copied_files.append(copy_path)
        return copied_files

    def __exit__(self, exc_type, exc_value, traceback):
        log_obj.info(f"Exiting folder: {self.folder_path}")
