class FolderHandlerError(Exception):
    """Custom exception for FolderHandlerError."""
    def __init__(self, msg="Retreaving python files error."):
        super().__init__(msg)

