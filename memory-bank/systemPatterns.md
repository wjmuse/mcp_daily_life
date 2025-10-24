# System Patterns: Document Assistant MCP Server

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────┐
│         MCP Client (Cline)              │
└─────────────┬───────────────────────────┘
              │ stdio
              ↓
┌─────────────────────────────────────────┐
│      MCP Server (server.py)             │
│  ┌─────────────────────────────────┐   │
│  │  Tool Handlers                  │   │
│  │  - index_document               │   │
│  │  - create_note                  │   │
│  │  - search_documents             │   │
│  │  - extract_metadata             │   │
│  └─────────────┬───────────────────┘   │
└────────────────┼───────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│   Document Processor                    │
│   (document_processor.py)               │
│  ┌─────────────────────────────────┐   │
│  │  - Index Management             │   │
│  │  - File Operations              │   │
│  │  - Search Logic                 │   │
│  │  - Metadata Extraction          │   │
│  └─────────────┬───────────────────┘   │
└────────────────┼───────────────────────┘
                 │
        ┌────────┴────────┐
        ↓                 ↓
┌──────────────┐  ┌──────────────┐
│ File System  │  │  JSON Index  │
│ (documents/) │  │  (index/)    │
└──────────────┘  └──────────────┘
```

## Key Technical Decisions

### 1. MCP Protocol via stdio
**Decision**: Use stdio transport for MCP communication
**Rationale**: 
- Standard MCP approach
- Simple to implement
- Works well with Cline
- No network configuration needed

### 2. File System Storage
**Decision**: Store documents and index on local file system
**Rationale**:
- Simple, no external dependencies
- Fast for small-medium collections
- Easy to backup and inspect
- Human-readable index (JSON)
**Trade-off**: May not scale to thousands of documents

### 3. JSON-Based Index
**Decision**: Use JSON file for document index
**Rationale**:
- Human-readable
- Easy to debug
- No database setup
- Python built-in support
**Trade-off**: Entire index loaded into memory

### 4. Async/Await Pattern
**Decision**: Use async I/O throughout
**Rationale**:
- MCP SDK expects async
- Better concurrency
- Non-blocking operations
- Future-proof for scaling

### 5. Tag-Based Organization
**Decision**: Use flat tags instead of hierarchical categories
**Rationale**:
- More flexible than rigid hierarchy
- Easy to filter and combine
- Natural for search
- User-friendly

## Design Patterns

### 1. Facade Pattern
**Location**: `DocumentProcessor` class
**Purpose**: Simplifies document operations for server
**Implementation**:
```python
class DocumentProcessor:
    def __init__(self):
        self.storage_dir = Path("./documents")
        self.index_dir = Path("./index")
        self.index = self._load_index()
    
    async def index_document(...) -> str
    async def create_note(...) -> str
    async def search_documents(...) -> List[Dict]
    async def extract_metadata(...) -> Dict
```

### 2. Repository Pattern
**Location**: Index management in `DocumentProcessor`
**Purpose**: Abstract data access layer
**Implementation**:
- `_load_index()`: Load data
- `_save_index()`: Persist data
- Index acts as in-memory repository

### 3. Custom Exception Hierarchy
**Location**: `errors.py`
**Purpose**: Specific error types for different failures
**Hierarchy**:
```
DocumentError (base)
├── DocumentNotFoundError
├── DocumentFormatError
├── DocumentIndexError
└── DocumentSearchError
```

### 4. Factory Pattern (Implicit)
**Location**: Note creation in `create_note`
**Purpose**: Standardized note creation with frontmatter
**Implementation**: Generates consistent markdown structure

## Component Relationships

### Server ↔ Document Processor
- **Relationship**: Delegation
- **Interaction**: Server calls processor methods
- **Data Flow**: Tool arguments → Processor → Results
- **Error Handling**: Processor exceptions caught by server

### Document Processor ↔ File System
- **Relationship**: Data Access
- **Interaction**: Async read/write operations
- **Data Flow**: Path → File content/metadata
- **Error Handling**: Custom exceptions for file issues

### Document Processor ↔ Index
- **Relationship**: State Management
- **Interaction**: Load on init, update in memory, save on changes
- **Data Structure**:
```json
{
  "documents": {
    "doc_id": {metadata}
  },
  "tags": {
    "tag_name": ["doc_id1", "doc_id2"]
  }
}
```

## Critical Implementation Paths

### 1. Document Indexing Flow
```
1. Validate file exists
2. Read file content (async)
3. Generate document ID (absolute path)
4. Extract metadata (size, timestamps, etc)
5. Update documents dict in index
6. Update tag references in index
7. Save index to disk
8. Return document ID
```

### 2. Search Flow
```
1. Normalize query (lowercase)
2. If tags provided:
   - Get candidate doc IDs from tag index
   - Intersect tag results
3. Else:
   - Consider all documents
4. For each candidate:
   - Check filename match
   - Check tag match
5. Limit results
6. Return metadata list
```

### 3. Note Creation Flow
```
1. Generate filename from title
2. Create frontmatter with metadata
3. Combine frontmatter + content
4. Write to documents directory (async)
5. Index the new note
6. Return file path
```

### 4. Error Handling Flow
```
1. Operation attempted
2. If error occurs:
   - Catch specific exception type
   - Log with context
   - Return error message in MCP response
3. Never expose stack traces to user
4. Always provide actionable error message
```

## Data Flow Patterns

### Index Update Pattern
```python
# Load → Modify → Save
index = self._load_index()
index["documents"][doc_id] = metadata
for tag in tags:
    index["tags"][tag].append(doc_id)
self._save_index()
```

### Async File Operations
```python
# Always use async for I/O
async def read_file(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
```

### Path Management
```python
# Use Path for cross-platform
from pathlib import Path
doc_path = Path(path).absolute()
```

## Scalability Considerations

### Current Limitations
- Index loaded entirely in memory
- Linear search through documents
- No pagination
- Single-threaded index updates

### Future Improvements
- Implement index caching
- Add pagination to search
- Consider SQLite for larger collections
- Implement full-text search
- Add relevance scoring
