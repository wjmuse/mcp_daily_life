# Documentation Requirements

## General Guidelines

- All code must be well-documented with clear, concise comments
- Update documentation whenever code changes are made
- Documentation should explain "why" not just "what"

## README.md

- Must include project overview and purpose
- Installation instructions with prerequisites
- Usage examples with code snippets
- Configuration options
- API documentation or links to it
- Contributing guidelines
- License information

## Code Documentation

### Docstrings

All public modules, classes, and functions must have docstrings following Google style:

```python
def function_name(param1: str, param2: int) -> bool:
    """Brief description of function.

    Longer description if needed, explaining the purpose and behavior.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: Description of when this error is raised
    """
    pass
```

### Inline Comments

- Use sparingly for complex logic
- Explain non-obvious decisions
- Keep comments up-to-date with code changes

## API Documentation

- Document all MCP tools with:
  - Tool name and purpose
  - Input parameters with types
  - Return values with types
  - Example usage
  - Error conditions

## Changelog

- Maintain CHANGELOG.md following Keep a Changelog format
- Document all notable changes
- Group changes by type (Added, Changed, Deprecated, Removed, Fixed, Security)
- Include version numbers and dates
