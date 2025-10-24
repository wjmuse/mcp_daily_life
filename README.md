# Document Assistant MCP Server

A Model Context Protocol (MCP) server for document processing, note-taking, and knowledge management. This server provides tools for indexing documents, creating notes, searching content, and extracting metadata.

## Features

- **Document Indexing**: Index documents for fast search and retrieval
- **Note Taking**: Create and organize markdown notes with tags
- **Search**: Search indexed documents by keywords and tags
- **Metadata Extraction**: Extract metadata from documents automatically

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Setup

1. Clone or download this repository to your workspace

2. Activate your Python virtual environment:
```bash
source myvenv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install the package in development mode:
```bash
pip install -e .
```

## Project Structure

```
.
├── .clinerules/              # Cline rules for coding standards
│   ├── 01-coding.md          # Core coding standards
│   ├── 02-documentation.md   # Documentation requirements
│   └── current-sprint.md     # Current sprint rules
├── memory-bank/              # Cline Memory Bank
│   ├── common-knowledge/     # Document format knowledge
│   ├── code-snippets/        # Reusable code patterns
│   └── configuration/        # Configuration settings
├── src/
│   └── document_assistant/   # Main package
│       ├── server.py         # MCP server implementation
│       └── utils/            # Utility modules
│           ├── errors.py              # Custom exceptions
│           └── document_processor.py  # Document processing logic
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup configuration
└── README.md                 # This file
```

## Usage

### Starting the Server

Run the MCP server using Python:

```bash
python -m document_assistant.server
```

Or use the installed console script:

```bash
document-assistant
```

### Available Tools

#### 1. index_document

Index a document for search and retrieval.

**Parameters:**
- `path` (required): Path to the document to index
- `tags` (optional): Array of tags for categorization

**Example:**
```json
{
  "path": "/path/to/document.md",
  "tags": ["work", "project"]
}
```

#### 2. create_note

Create a new note in markdown format.

**Parameters:**
- `title` (required): Title of the note
- `content` (required): Content of the note in markdown
- `tags` (optional): Array of tags for the note

**Example:**
```json
{
  "title": "Meeting Notes",
  "content": "## Discussion Points\n\n- Item 1\n- Item 2",
  "tags": ["meeting", "2024"]
}
```

#### 3. search_documents

Search indexed documents by keywords or tags.

**Parameters:**
- `query` (required): Search query string
- `tags` (optional): Array of tags to filter results
- `limit` (optional): Maximum number of results (default: 10)

**Example:**
```json
{
  "query": "meeting",
  "tags": ["work"],
  "limit": 5
}
```

#### 4. extract_metadata

Extract metadata from a document.

**Parameters:**
- `path` (required): Path to the document

**Example:**
```json
{
  "path": "/path/to/document.md"
}
```

## Configuration

### Storage Locations

- Documents: `./documents` (created automatically)
- Index: `./index` (created automatically)
- Backups: `./backups` (if enabled)

### Supported File Formats

- Markdown (.md)
- Plain text (.txt)
- JSON (.json)

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows PEP 8 coding standards. Use the following tools for code quality:

```bash
# Format code
black src/

# Check style
flake8 src/

# Type checking
mypy src/
```

## MCP Configuration

To use this server with Cline or other MCP clients, add it to your MCP settings:

```json
{
  "mcpServers": {
    "document-assistant": {
      "command": "python",
      "args": ["-m", "document_assistant.server"],
      "cwd": "/home/wjmuse/workspace/mcp_daily_life"
    }
  }
}
```

## Memory Bank

The `memory-bank/` directory contains custom instructions for Cline:

- **common-knowledge/**: Document format knowledge and best practices
- **code-snippets/**: Reusable MCP patterns and code examples
- **configuration/**: Server settings and preferences

## Contributing

1. Follow the coding standards in `.clinerules/01-coding.md`
2. Update documentation as per `.clinerules/02-documentation.md`
3. Check current sprint rules in `.clinerules/current-sprint.md`

## License

MIT License

## Troubleshooting

### Import Errors

If you encounter import errors, ensure:
1. Virtual environment is activated
2. Dependencies are installed: `pip install -r requirements.txt`
3. Package is installed in development mode: `pip install -e .`

### Path Issues

- Use absolute paths when possible
- Ensure document paths are accessible
- Check file permissions

## Support

For issues and questions, please refer to:
- `.clinerules/` directory for development guidelines
- `memory-bank/` directory for knowledge base
- MCP documentation: https://docs.cline.bot/mcp
