class InvalidFormatError(Exception):
    """Exception raised for invalid format errors."""

    def __init__(self, message: str):
        super().__init__(message)


class DatasetNotFoundError(Exception):
    """Exception raised for invalid dataset errors."""

    def __init__(self, message: str):
        super().__init__(message)


class DatasetExistsError(Exception):
    """Exception raised for already existing dataset errors."""

    def __init__(self, message: str):
        super().__init__(message)
