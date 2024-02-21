# PyCode Error handler module

# Description: A Python module providing custom exception classes
#              for handling errors and exceptions within the PyCode
#              style checking and corrective modules.

# Created by: Stjepan Prakljačić
# License: MIT License, all rights reserved.
# Repository: https://github.com/StjepanPrakljacic/PEP8-parser.git
#
# Version: 1.0.0
###############################################################################


class FolderHandlerError(Exception):
    """
    A custom exception class for handling errors related to the FolderHandler.

    Attributes:
        msg (str): The error message.

    Usage:
        try:
            # Code that may raise FolderHandlerError
        except FolderHandlerError as folder_error:
            print(f"Error: {folder_error}")
    """

    def __init__(self, msg="Retreaving python files error."):
        super().__init__(msg)


class CodeStyleAnalysisError(Exception):
    """
    Custom exception class for handling code style analysis errors.
    """
    pass
