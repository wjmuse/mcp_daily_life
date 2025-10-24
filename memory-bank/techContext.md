# Technical Context: Document Assistant MCP Server

## Technologies Used

### Core Technologies

#### Python 3.12
- **Purpose**: Primary programming language
- **Version**: 3.12.x (minimum 3.10)
- **Key Features Used**:
  - Type hints for clarity
  - Async/await for I/O
  - Pathlib for file operations
  - JSON for data serialization

#### MCP SDK (1.19.0)
- **Purpose**: Model Context Protocol implementation
- **Package**: `mcp>=1.0.0`
- **Key Components**:
  - `mcp.server`: Server implementation
  - `mcp.types`: Type definitions for tools
  - `mcp.server.stdio`: stdio transport
  - `mcp.server.models`: Initialization options

### Dependencies

```
mcp>=1.0.0              # Core MCP functionality
├── anyio>=4.5          # Async I/O abstractions
├── httpx>=0.27.1       # HTTP client (for MCP)
├── httpx-sse>=0.4      # Server-sent events
├── jsonschema>=4.20.0  # JSON validation
├── pydantic>=2.11.0    # Data validation
├── starlette>=0.27     # ASGI framework
└── uvicorn>=0.31.1     # ASGI server
```

### Standard Library Usage

- `asyncio`: Async event loop and coroutines
- `json`: Index serialization/deserialization
- `logging`: Application logging
- `pathlib`: Cross-platform path handling
- `datetime`: Timestamp management
- `typing`: Type annotations

## Development Setup

### Project Structure
```
/home/wjmuse/workspace/mcp_daily_life/
├── myvenv/                    # Virtual environment
├── src/document_assistant/    # Source code
│   ├── __init__.py
│   ├── server.py             # MCP server
│   └── utils/
│       ├── __init__.py
│       ├── errors.py         # Exceptions
│       └── document_processor.py
├── requirements.txt           # Dependencies
├── setup.py                  # Package config
└── README.md                 # Documentation
```

### Virtual Environment
- **Location**: `/home/wjmuse/workspace/mcp_daily_life/myvenv/`
- **Activation**: `source myvenv/bin/activate`
- **Purpose**: Isolated dependency management
- **Python**: 3.12.x

### Installation Commands
```bash
# Create virtual environment
python3 -m venv myvenv

# Activate
source myvenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

## Technical Constraints

### File System Requirements
- **Working Directory**: `/home/wjmuse/workspace/mcp_daily_life`
- **Document Storage**: `./documents/` (auto-created)
- **Index Storage**: `./index/` (auto-created)
- **Permissions**: Read/write access required

### Memory Constraints
- Index loaded entirely in memory
- Suitable for up to ~1000 documents
- Memory usage scales with index size
- Consider limits for large collections

### Performance Characteristics
- **Indexing**: O(1) - single file operation
- **Search**: O(n) - linear through documents
- **Tag Lookup**: O(1) - dictionary lookup
- **Index Load**: O(n) - full file read

### Platform Compatibility
- **OS**: Linux (developed on Linux 6.6)
- **Shell**: Bash
- **Architecture**: x86_64
- **Encoding**: UTF-8 (assumed for all files)

## Tool Usage Patterns

### Running the Server

#### Direct Execution
```bash
python -m document_assistant.server
```

#### Via Console Script
```bash
document-assistant
```

#### MCP Configuration (Cline)
```json
{
  "mcpServers": {
    "document-assistant": {
      "command": "python",
      "args": ["-m", "document_assistant.server"],
      "cwd": "/home/wjmuse/workspace/mcp_daily_life",
      "env": {
        "PATH": "/home/wjmuse/workspace/mcp_daily_life/myvenv/bin"
      }
    }
  }
}
```

### Development Tools

#### Code Quality
```bash
# Format code
black src/

# Type checking
mypy src/

# Linting
flake8 src/
```

#### Testing
```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=document_assistant tests/
```

## Data Storage Formats

### Index File (documents.json)
```json
{
  "documents": {
    "/absolute/path/to/doc.md": {
      "id": "/absolute/path/to/doc.md",
      "path": "/absolute/path/to/doc.md",
      "filename": "doc.md",
      "extension": ".md",
      "size": 1234,
      "created": "2024-10-24T14:26:00",
      "modified": "2024-10-24T14:26:00",
      "tags": ["tag1", "tag2"],
      "indexed_at": "2024-10-24T14:26:00"
    }
  },
  "tags": {
    "tag1": ["/path/to/doc1.md", "/path/to/doc2.md"],
    "tag2": ["/path/to/doc1.md"]
  }
}
```

### Note Format (Markdown with Frontmatter)
```markdown
---
title: Note Title
created: 2024-10-24T14:26:00
tags: tag1, tag2
---

# Content here

Markdown content...
```

## Logging Configuration

### Default Setup
```python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Log Levels
- **DEBUG**: Detailed information for debugging
- **INFO**: General operational events
- **WARNING**: Warning messages
- **ERROR**: Error events
- **CRITICAL**: Critical problems

### Log Locations
- Console output (stderr)
- No file logging by default

## Environment Variables

### Optional Configuration
- None required for basic operation
- MCP client may set environment variables
- PATH must include Python and dependencies

## Security Considerations

### Current Implementation
- No authentication/authorization
- Local file system access only
- No network exposure (stdio only)
- No input sanitization beyond basic validation
- Trust MCP client completely

### Future Security Enhancements
- Input validation/sanitization
- Path traversal protection
- File size limits
- Rate limiting
- Access control

## Version Compatibility

### Python Versions
- **Required**: 3.10+
- **Tested**: 3.12.x
- **Features Used**:
  - Type hints (3.5+)
  - Async/await (3.5+)
  - f-strings (3.6+)
  - pathlib (3.4+)

### MCP Protocol
- **Version**: 2024-11-05
- **Transport**: stdio
- **Features**: Tools only (no resources or prompts)

## Known Technical Limitations

1. **Index in Memory**: Entire index loaded at startup
2. **Linear Search**: No indexing for search optimization
3. **No Concurrency**: Single-threaded index updates
4. **No Transactions**: Index updates not atomic
5. **No Backup**: No automatic backup mechanism
6. **UTF-8 Only**: Assumes UTF-8 encoding
7. **Local Only**: No remote storage support
