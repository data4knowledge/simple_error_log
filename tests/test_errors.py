import re
from simple_error_log.errors import Errors
from simple_error_log.error import Error
from simple_error_log.error_location import ErrorLocation


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
    errors.add("Test error", location, "test_error_type", Error.ERROR)
    assert errors.count() == 1


def test_errors_clear():
    """
    Test the errors clear method
    """
    errors = Errors()
    location = MockErrorLocation()
    errors.add("Test error", location, "test_error_type", Error.ERROR)
    errors.clear()
    assert errors.count() == 0


def test_errors_dump():
    """
    Test the errors dump method
    """
    errors = Errors()
    location = MockErrorLocation()
    errors.add("Test error 1", location, "warning_type", Error.WARNING)
    errors.add("Test error 2", location, "error_type", Error.ERROR)
    
    # With the new logic, dump(Error.WARNING) returns errors with level >= WARNING
    # So it should include both ERROR and WARNING levels
    dumped_errors = errors.dump(Error.WARNING)
    assert len(dumped_errors) == 2
    
    # dump(Error.ERROR) returns errors with level >= ERROR
    # So it should include only the ERROR level
    dumped_errors = errors.dump(Error.ERROR)
    assert len(dumped_errors) == 1
    
    # Test the default parameter (ERROR)
    dumped_errors = errors.dump()
    assert len(dumped_errors) == 1


def test_errors_error():
    """
    Test the error method
    """
    errors = Errors()
    location = MockErrorLocation()
    errors.error("Test error message", location)
    
    assert errors.count() == 1
    
    # Get the error and verify its properties
    dumped_errors = errors.dump(Error.ERROR)
    assert len(dumped_errors) == 1
    
    error = dumped_errors[0]
    assert error["message"] == "Test error message"
    assert error["level"] == "Error"
    assert error["location"] == {"mock_key": "mock_value"}


def test_errors_info():
    """
    Test the info method
    """
    errors = Errors()
    location = MockErrorLocation()
    errors.info("Test info message", location)
    
    assert errors.count() == 1
    
    # With the new logic, INFO level errors are only included when dumping with level <= INFO
    # INFO level errors should not be included when dumping with ERROR or WARNING levels
    dumped_errors = errors.dump(Error.ERROR)
    assert len(dumped_errors) == 0
    
    dumped_errors = errors.dump(Error.WARNING)
    assert len(dumped_errors) == 0
    
    # But they should be included when dumping with INFO or DEBUG levels
    dumped_errors = errors.dump(Error.INFO)
    assert len(dumped_errors) == 1
    
    error = dumped_errors[0]
    assert error["message"] == "Test info message"
    assert error["level"] == "Info"
    assert error["location"] == {"mock_key": "mock_value"}
    
    dumped_errors = errors.dump(Error.DEBUG)
    assert len(dumped_errors) == 1


def test_errors_debug():
    """
    Test the debug method
    """
    errors = Errors()
    location = MockErrorLocation()
    errors.debug("Test debug message", location)
    
    assert errors.count() == 1
    
    # With the new logic, DEBUG level errors are only included when dumping with level <= DEBUG
    # DEBUG level errors should not be included when dumping with ERROR, WARNING, or INFO levels
    dumped_errors = errors.dump(Error.ERROR)
    assert len(dumped_errors) == 0
    
    dumped_errors = errors.dump(Error.WARNING)
    assert len(dumped_errors) == 0
    
    dumped_errors = errors.dump(Error.INFO)
    assert len(dumped_errors) == 0
    
    # But they should be included when dumping with DEBUG level
    dumped_errors = errors.dump(Error.DEBUG)
    assert len(dumped_errors) == 1
    
    error = dumped_errors[0]
    assert error["message"] == "Test debug message"
    assert error["level"] == "Debug"
    assert error["location"] == {"mock_key": "mock_value"}


def test_errors_warning():
    """
    Test the warning method
    """
    errors = Errors()
    location = MockErrorLocation()
    errors.warning("Test warning message", location)
    
    assert errors.count() == 1
    
    # With the new logic, WARNING level errors are only included when dumping with level <= WARNING
    # WARNING level errors should not be included when dumping with ERROR level
    dumped_errors = errors.dump(Error.ERROR)
    assert len(dumped_errors) == 0
    
    # But they should be included when dumping with WARNING, INFO, or DEBUG levels
    dumped_errors = errors.dump(Error.WARNING)
    assert len(dumped_errors) == 1
    
    error = dumped_errors[0]
    assert error["message"] == "Test warning message"
    assert error["level"] == "Warning"
    assert error["location"] == {"mock_key": "mock_value"}
    
    dumped_errors = errors.dump(Error.INFO)
    assert len(dumped_errors) == 1
    
    dumped_errors = errors.dump(Error.DEBUG)
    assert len(dumped_errors) == 1


def test_errors_exception():
    """
    Test the exception method
    """
    errors = Errors()
    location = MockErrorLocation()
    
    try:
        # Create an exception
        raise ValueError("Test exception")
    except Exception as e:
        errors.exception("Test exception message", e, location)
    
    assert errors.count() == 1
    
    # Get the error and verify its properties
    dumped_errors = errors.dump(Error.ERROR)
    assert len(dumped_errors) == 1
    
    error = dumped_errors[0]
    # Check that the message contains the expected parts
    assert "Test exception message" in error["message"]
    assert "Details" in error["message"]
    assert "ValueError: Test exception" in error["message"]
    assert "Traceback" in error["message"]
    assert error["level"] == "Error"
    assert error["location"] == {"mock_key": "mock_value"}


def test_errors_with_default_location():
    """
    Test the methods with default location (None)
    """
    errors = Errors()
    
    # Test each method with default location
    errors.error("Test error with default location")
    errors.info("Test info with default location")
    errors.debug("Test debug with default location")
    errors.warning("Test warning with default location")
    
    try:
        raise ValueError("Test exception")
    except Exception as e:
        errors.exception("Test exception with default location", e)
    
    assert errors.count() == 5
    
    # Verify that all errors have a default location
    # With the new logic, we need to use the lowest level (DEBUG) to get all errors
    dumped_errors = errors.dump(Error.DEBUG)
    assert len(dumped_errors) == 5
    for error in dumped_errors:
        assert "location" in error
        # Default ErrorLocation to_dict() should return an empty dict
        assert isinstance(error["location"], dict)
