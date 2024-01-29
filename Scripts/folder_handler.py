import os
import shutil
from .logging_handler import log_obj
from .error_handler import FolderHandlerError

class FolderHandler:
    """
    A class representing a context manager for managing a folder.

    Attributes:
        folder_path (str): The path to the folder to be managed.
        success (bool): Indicates whether the folder management was successful.

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
            # The 'success' attribute indicates whether the folder management
              was successful.
        # The folder context has been exited.
    """
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.success = False

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
        self.success = bool(copied_files)
        return copied_files

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.success:
            raise FolderHandlerError(
                f"No .py files were found in the folder: {self.folder_path}"
                )
        else:
            log_obj.info(f"Exiting folder: {self.folder_path}")




