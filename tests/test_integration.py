from simple_error_log.error_location import (
    GridLocation,
    DocumentSectionLocation,
)
from simple_error_log.errors import Errors


def test_integration():
    errors = Errors()
    location = DocumentSectionLocation("1", "Introduction")
    errors.add("Test error 1", location, "section_error")
    location = GridLocation(1, 3)
    errors.add("Test error 2", location, "grid_error")
    location = GridLocation(10, 30)
    errors.add("Test error 3", location, "info_error", level=Errors.INFO)
    assert errors.count() == 3
    assert errors.dump(Errors.ERROR) == [
        {
            "location": {"section_number": "1", "section_title": "Introduction"},
            "message": "Test error 1",
            "level": "Error",
            "type": "section_error",
        },
        {
            "location": {"row": 1, "column": 3},
            "message": "Test error 2",
            "level": "Error",
            "type": "grid_error",
        },
        {
            "location": {"row": 10, "column": 30},
            "message": "Test error 3",
            "level": "Info",
            "type": "info_error",
        },
    ]
    assert errors.dump(Errors.INFO) == [
        {
            "location": {"row": 10, "column": 30},
            "message": "Test error 3",
            "level": "Info",
            "type": "info_error",
        }
    ]
