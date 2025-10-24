# Project Brief: Document Assistant MCP Server

## Project Overview

An MCP (Model Context Protocol) server implementation in Python that provides document processing, note-taking, and knowledge management capabilities for Cline and other MCP clients.

## Core Requirements

### Primary Goals
1. Enable document indexing and search functionality
2. Provide note creation and organization tools
3. Support metadata extraction from documents
4. Maintain searchable document index

### Key Features
- **Document Indexing**: Index documents with metadata and tags
- **Note Creation**: Create markdown notes with frontmatter
- **Search**: Keyword and tag-based document search
- **Metadata Extraction**: Extract file information and metadata

## Project Scope

### In Scope
- MCP server with stdio transport
- Basic document processing (markdown, text, JSON)
- File-system based storage
- JSON index for search
- Tag-based organization
- Async I/O operations

### Out of Scope (for v0.1.0)
- Database integration
- Full-text search
- Document conversion between formats
- Cloud storage
- Multi-user support
- Authentication/authorization

## Success Criteria

1. Server successfully starts and communicates via MCP protocol
2. All 4 tools (index_document, create_note, search_documents, extract_metadata) work correctly
3. Documents can be indexed and retrieved
4. Search returns relevant results
5. Code follows Python best practices (PEP 8)
6. Basic error handling in place

## Technical Constraints

- Python 3.10 or higher
- MCP SDK 1.0+
- File system as primary storage
- Must work in `/home/wjmuse/workspace/mcp_daily_life`
- Virtual environment: `myvenv/`

## Project Context

This is a minimal working implementation focused on core functionality rather than advanced features. The goal is to provide a solid foundation that can be extended later with additional capabilities like full-text search, format conversion, and database backends.
