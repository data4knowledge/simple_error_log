import logging
from simple_error_log.error_location import ErrorLocation


class Error:
    """
    Base class for errors
    """

    ERROR = logging.ERROR
    WARNING = logging.WARNING
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    LABEL = {ERROR: "error", WARNING: "warning", DEBUG: "debug", INFO: "info"}

    def __init__(self, message: str, location: ErrorLocation, error_type: str = "", level: int = ERROR):
        """
        Initialize the error
        """
        self.location = location
        self.message = message
        self.level = level
        self.error_type = error_type

    def to_dict(self) -> dict:
        """
        Convert the error to a dictionary
        """
        result = {
            "level": self.__class__.LABEL[self.level].capitalize(),
            "message": self.message,
            "type": self.error_type,
            "location": self.location.to_dict(),
        }
        return result
