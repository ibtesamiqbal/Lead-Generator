# Python Coding Standards

## Standards & Style Guide
1. **Python Version**: Python 3.11+ / 3.12 syntax.
2. **Type Hints**: Mandatory type annotations on all function signatures, parameters, and return types.
3. **Data Schemas**: Use Pydantic v2 `BaseModel` for validation, serialization, and settings management.
4. **Formatting**: Follow PEP 8 guidelines (4 spaces indentation, max 100 char line length).
5. **Docstrings**: Provide Google-style docstrings for all classes, methods, and functions.
6. **Logging**: Use structured logger instead of `print()` statements.
7. **Error Handling**: Raise domain-specific custom exceptions; never catch bare `Exception` without context logging.
