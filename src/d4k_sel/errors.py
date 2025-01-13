from d4k_sel.error import Error
from d4k_sel.error_location import ErrorLocation


class Errors:
    """
    Class for logging errors
    """
    ERROR = Error.ERROR # 40    
    WARNING = Error.WARNING # 30
    DEBUG = Error.DEBUG # 20
    INFO = Error.INFO # 10

    def __init__(self):
        """
        Initialize the errors
        """
        self._items: list[Error] = []

    def clear(self):
        """
        Clear the errors
        """
        self._items = []

    def add(
        self, message: str, location: ErrorLocation, level: int = Error.ERROR
    ) -> None:
        """
        Add an error
        """
        error = Error(message, location, level)
        self._items.append(error)

    def count(self) -> int:
        """
        Count the errors
        """
        return len(self._items)

    def dump(self, level) -> list:
        """
        Dump the errors
        """
        result = []
        for item in self._items:
            print(f"LEVEL: {item.level}, {level}")
            if item.level <= level:
                result.append(item.to_dict())
        return result
