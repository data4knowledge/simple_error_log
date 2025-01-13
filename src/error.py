import logging
from error_location import ErrorLocation


class Error:
    """
    Base class for errors
    """
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    LABEL = {ERROR: "error", WARNING: "warning", DEBUG: "debug", INFO: "info"}

    def __init__(self, message: str, location: ErrorLocation, level: int = ERROR):
        """
        Initialize the error
        """
        self.location = location
        self.message = message
        self.level = level

    def to_dict(self) -> dict:
        """
        Convert the error to a dictionary
        """
        return {
            **self.location.to_dict(),
            **{
                "message": self.message,
                "level": self.__class__.LABEL[self.level].capitalize(),
            },
        }
