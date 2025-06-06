import traceback
from simple_error_log.error import Error
from simple_error_log.error_location import ErrorLocation


class Errors:
    """
    Class for logging errors
    """

    ERROR = Error.ERROR  # 40
    WARNING = Error.WARNING  # 30
    DEBUG = Error.DEBUG  # 20
    INFO = Error.INFO  # 10

    def __init__(self):
        self._items: list[Error] = []

    def error(self, message: str, location: ErrorLocation = None):
        self.add(message, location)

    def info(self, message: str, location: ErrorLocation = None):
        self.add(message, location, level=self.INFO)

    def debug(self, message: str, location: ErrorLocation = None):
        self.add(message, location, level=self.DEBUG)

    def warning(self, message: str, location: ErrorLocation = None):
        self.add(message, location, level=self.WARNING)

    def exception(self, message: str, e: Exception, location: ErrorLocation = None):
        message = f"{message}\n\nDetails\n{e}\n\nTraceback\n{traceback.format_exc()}"
        self.add(message, location)

    def merge(self, other: 'Errors'):
        self._items += other._items
        self._items = sorted(self._items, key=lambda d: d.timestamp)
        
    def clear(self):
        self._items = []

    def add(
        self,
        message: str,
        location: ErrorLocation = None,
        error_type: str = "",
        level: int = Error.ERROR,
    ) -> None:
        location = location if location else ErrorLocation()
        error = Error(message, location, error_type, level)
        self._items.append(error)

    def count(self) -> int:
        return len(self._items)

    def error_count(self) -> int:
        return len([x for x in self._items if x.level == Error.ERROR])

    def dump(self, level=ERROR) -> list:
        result = []
        for item in self._items:
            if item.level >= level:
                result.append(item.to_dict())
        return result
