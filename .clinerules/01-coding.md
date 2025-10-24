# Coding Standards

## Python Style Guide

- Follow PEP 8 for Python code style
- Use type hints for function parameters and return values
- Maximum line length: 88 characters (Black formatter default)
- Use meaningful variable and function names

## Code Organization

- Use absolute imports over relative imports where possible
- Group imports in the following order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application imports
- Separate each import group with a blank line

## Error Handling

- Use custom exceptions defined in `utils/errors.py`
- Always provide meaningful error messages
- Log errors appropriately with context
- Handle edge cases explicitly

## Testing

- Write unit tests for all business logic
- Use pytest for testing framework
- Maintain at least 80% code coverage
- Mock external dependencies in tests

## Documentation

- Use docstrings for all public modules, classes, and functions
- Follow Google-style docstring format
- Include examples in docstrings where helpful
- Keep README.md up to date with API changes

## Version Control

- Write clear, descriptive commit messages
- Use feature branches for development
- Keep commits atomic and focused
- Reference issues in commit messages where applicable
