from d4k_sel.errors import Errors
from d4k_sel.error import Error
from d4k_sel.error_location import ErrorLocation


class MockErrorLocation(ErrorLocation):
    """
    Mock error location
    """
    def to_dict(self):
        return {"mock_key": "mock_value"}


def test_errors_initialization():
    """
    Test the errors initialization
    """
    errors = Errors()
    assert errors.count() == 0


def test_errors_add():
    """
    Test the errors add method
    """
    errors = Errors()
    location = MockErrorLocation()
    errors.add("Test error", location, Error.ERROR)
    assert errors.count() == 1


def test_errors_clear():
    """
    Test the errors clear method
    """
    errors = Errors()
    location = MockErrorLocation()
    errors.add("Test error", location, Error.ERROR)
    errors.clear()
    assert errors.count() == 0


def test_errors_dump():
    """
    Test the errors dump method
    """
    errors = Errors()
    location = MockErrorLocation()
    errors.add("Test error 1", location, Error.WARNING)
    errors.add("Test error 2", location, Error.ERROR)
    dumped_errors = errors.dump(Error.WARNING)
    assert len(dumped_errors) == 1  # Both errors should be included
    dumped_errors = errors.dump(Error.ERROR)
    assert len(dumped_errors) == 2  # Only the second error should be included
