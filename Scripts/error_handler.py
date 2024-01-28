from .logging_handler import log_obj

class FolderHandlerError(Exception):
    """Custom exception for FolderHandler errors."""

    def __init__(self, msg=None):
        if msg is not None:
            log_obj.error(msg)
        else:
            log_obj.error("An error occurred in FolderHandler: No .py files found.")
        super().__init__(msg)