# Simple Error Log

A lightweight Python library for structured error logging with location context. Collect, organize, and serialize errors with severity levels and rich location metadata—perfect for validation systems, data pipelines, and document processing.

## Features

- **Zero dependencies** - Pure Python standard library
- **Multiple severity levels** - ERROR, WARNING, INFO, DEBUG
- **Location tracking** - Grid coordinates, document sections, class methods, or custom locations
- **Exception capture** - Full traceback and call stack preservation
- **Structured extras** - Attach machine-readable payloads alongside the human message
- **Flexible output** - Dictionary (JSON-serializable) or formatted strings
- **Error aggregation** - Merge, filter, and query error collections

## Installation

```bash
pip install simple_error_log
```

Requires Python 3.10+

## Quick Start

```python
from simple_error_log import Errors, DocumentSectionLocation, GridLocation

# Create an error collection
errors = Errors()

# Log errors with locations
location = DocumentSectionLocation("2.1", "Data Validation")
errors.error("Missing required field: email", location)

# Different severity levels
errors.warning("Deprecated format detected")
errors.info("Processing started")
errors.debug("Parsed 150 records")

# Log exceptions with full context
try:
    process_data()
except Exception as e:
    errors.exception("Processing failed", e, location)

# Export errors
print(errors.dump())  # Formatted string output
data = errors.to_dict()  # JSON-serializable dict
```

## Core Classes

### `Errors`

The main collection class for managing multiple errors.

```python
from simple_error_log import Errors

errors = Errors()

# Add errors at different levels
errors.error("Critical failure")
errors.warning("Non-critical issue")
errors.info("Informational message")
errors.debug("Debug details")

# Log exceptions with traceback
try:
    risky_operation()
except Exception as e:
    errors.exception("Operation failed", e)

# Query the collection
errors.count()        # Total number of logged items
errors.error_count()  # Only ERROR-level items

# Export with level filtering
errors.to_dict(Errors.ERROR)    # Only errors
errors.to_dict(Errors.WARNING)  # Errors and warnings
errors.dump(Errors.DEBUG)       # Everything, formatted

# Merge collections
combined = errors1.merge(errors2)  # Sorted by timestamp

# Clear all errors
errors.clear()
```

### `Error`

Represents a single error with metadata.

```python
from simple_error_log import Error, GridLocation

error = Error(
    message="Invalid value at position",
    location=GridLocation(row=5, column=3),
    level=Error.WARNING,
    error_type="validation"
)

print(error)           # Formatted string
error.to_dict()        # Dictionary representation
error.timestamp        # When it was created
```

**Severity Levels:**
- `Error.ERROR` (40) - Critical errors
- `Error.WARNING` (30) - Warnings
- `Error.DEBUG` (20) - Debug information
- `Error.INFO` (10) - Informational messages

### Structured Extras

Every logging method accepts an optional `extra` dict for machine-readable
context that downstream consumers shouldn't have to parse out of the message
string. It pairs naturally with `error_type` as a filter tag.

```python
from simple_error_log import Errors, GridLocation

errors = Errors()

errors.warning(
    "Normalised phase label",
    location=GridLocation(row=4, column=2),
    error_type="normalisation",
    extra={"source": "Phase III", "normalised": "Phase 3"},
)

# Available on every level plus exception()
errors.error("Invalid code", error_type="lookup", extra={"code": "X99"})
errors.info("Batch complete", extra={"records": 1500, "elapsed_ms": 842})
```

The payload round-trips through `to_dict()` under the `"extra"` key.

### Location Classes

#### `GridLocation`
For grid or table-based positions:

```python
from simple_error_log import GridLocation

loc = GridLocation(row=10, column=5)
print(loc)        # "[10, 5]"
loc.to_dict()     # {"row": 10, "column": 5}
```

#### `DocumentSectionLocation`
For document sections:

```python
from simple_error_log import DocumentSectionLocation

loc = DocumentSectionLocation("3.2", "Methodology")
print(loc)        # "[3.2 Methodology]"
loc.to_dict()     # {"section_number": "3.2", "section_title": "Methodology"}
```

#### `KlassMethodLocation`
For class methods:

```python
from simple_error_log import KlassMethodLocation

loc = KlassMethodLocation("DataParser", "validate")
print(loc)        # "DataParser.validate"
loc.to_dict()     # {"class_name": "DataParser", "method_name": "validate"}
```

#### Custom Locations
Create your own by subclassing `ErrorLocation`:

```python
from simple_error_log import ErrorLocation

class FileLocation(ErrorLocation):
    def __init__(self, filename: str, line: int):
        self.filename = filename
        self.line = line

    def to_dict(self) -> dict:
        return {"filename": self.filename, "line": self.line}

    def __str__(self) -> str:
        return f"{self.filename}:{self.line}"
```

## Example: Data Validation Pipeline

```python
from simple_error_log import Errors, GridLocation

def validate_spreadsheet(data: list[list]) -> Errors:
    errors = Errors()

    for row_idx, row in enumerate(data):
        for col_idx, cell in enumerate(row):
            location = GridLocation(row_idx, col_idx)

            if cell is None:
                errors.error("Empty cell not allowed", location)
            elif isinstance(cell, str) and len(cell) > 255:
                errors.warning("Cell content exceeds recommended length", location)

    return errors

# Usage
errors = validate_spreadsheet(my_data)

if errors.error_count() > 0:
    print("Validation failed:")
    print(errors.dump(Errors.ERROR))
else:
    print(f"Validation passed with {errors.count()} warnings")
```

## Output Formats

### `dump()` - Formatted String

```
error: Missing required field
  location: [2.1 Data Validation]
  timestamp: 2024-01-15 10:30:45

warning: Deprecated format detected
  timestamp: 2024-01-15 10:30:46
```

### `to_dict()` - JSON-Serializable

```python
[
    {
        "message": "Missing required field",
        "level": "error",
        "error_type": "",
        "location": {"section_number": "2.1", "section_title": "Data Validation"},
        "timestamp": "2024-01-15T10:30:45"
    }
]
```

## Development

### Running Tests

```bash
pip install pytest pytest-cov
pytest
```

### Building the Package

```bash
pip install build twine
python -m build
twine upload dist/*
```

## License

MIT
