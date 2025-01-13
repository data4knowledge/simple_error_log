from d4k_sel.error_location import (
    ErrorLocation,
    GridLocation,
    DocumentSectionLocation,
)


def test_error_location_str():
    gl = ErrorLocation()
    assert str(gl) == ""
    assert gl.format() == ""
    assert gl.to_dict() == {}


def test_grid_location_str():
    gl = GridLocation(1, 2)
    assert str(gl) == "[1, 2]"
    assert gl.to_dict() == {"row": 1, "column": 2}


def test_document_section_location_str():
    dsl = DocumentSectionLocation("1", "Introduction")
    assert str(dsl) == "[1 Introduction]"
    assert dsl.to_dict() == {"section_number": "1", "section_title": "Introduction"}
