from simple_error_log.error import Error
from simple_error_log.error_location import ErrorLocation


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
    error = Error("Test error message", location, "test_error_type", Error.ERROR)
    assert error.message == "Test error message"
    assert error.location == location
    assert error.level == Error.ERROR
    assert error.error_type == "test_error_type"


def test_error_to_dict():
    """
    Test the error to dictionary conversion
    """
    location = MockErrorLocation()
    error = Error("Test error message", location, "test_error_type", Error.WARNING)
    result_dict = error.to_dict()

    # Check each field individually, ignoring the timestamp
    assert result_dict["location"] == {"mock_key": "mock_value"}
    assert result_dict["message"] == "Test error message"
    assert result_dict["level"] == "Warning"
    assert result_dict["type"] == "test_error_type"

    # Verify timestamp is present and formatted correctly
    assert "timestamp" in result_dict
    assert isinstance(result_dict["timestamp"], str)
    # Check timestamp format (YYYY-MM-DD HH:MM:SS.ffffff)
    import re

    assert re.match(
        r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}", result_dict["timestamp"]
    )
