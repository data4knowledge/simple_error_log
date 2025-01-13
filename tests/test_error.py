from d4k_sel.error import Error
from d4k_sel.error_location import ErrorLocation


class MockErrorLocation(ErrorLocation):
    """
    Mock error location
    """
    def to_dict(self):
        return {"mock_key": "mock_value"}


def test_error_initialization():
    """
    Test the error initialization
    """
    location = MockErrorLocation()
    error = Error("Test error message", location, Error.ERROR)
    assert error.message == "Test error message"
    assert error.location == location
    assert error.level == Error.ERROR


def test_error_to_dict():
    """
    Test the error to dictionary conversion
    """
    location = MockErrorLocation()
    error = Error("Test error message", location, Error.WARNING)
    expected_dict = {
       "location": {"mock_key": "mock_value"},
        "message": "Test error message",
        "level": "Warning",
    }
    assert error.to_dict() == expected_dict
