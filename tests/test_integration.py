from d4k_sel.error_location import (
    GridLocation,
    DocumentSectionLocation,
)
from d4k_sel.errors import Errors

def test_integration():
    errors = Errors()
    location = DocumentSectionLocation("1", "Introduction")
    errors.add("Test error 1", location)
    location = GridLocation(1, 3)
    errors.add("Test error 2", location)
    location = GridLocation(10, 30)
    errors.add("Test error 3", location, level=Errors.INFO)
    assert errors.count() == 3
    assert errors.dump(Errors.ERROR) == [
        {
            "location": {"section_number": "1", "section_title": "Introduction"},
            "message": "Test error 1",
            'level': 'Error'
        },
        {
            "location": {"row": 1, "column": 3}, 
            "message": "Test error 2",
            'level': 'Error'
        },
        {
            "location": {"row": 10, "column": 30},
            "message": "Test error 3",
            'level': 'Info'
        }
    ]
    assert errors.dump(Errors.INFO) == [
        {
            "location": {"row": 10, "column": 30},
            "message": "Test error 3",
            'level': 'Info'
        }
    ]


