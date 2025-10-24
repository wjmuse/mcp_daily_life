"""MCP Server for Document Processing and Knowledge Management."""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
import mcp.types as types
from mcp.server.stdio import stdio_server

from .utils.errors import DocumentError
from .utils.document_processor import DocumentProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize server
server = Server("document-assistant")

# Initialize document processor
doc_processor = DocumentProcessor()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools for document processing and knowledge management.
    
    Returns:
        List of available tools with their schemas.
    """
    return [
        types.Tool(
            name="index_document",
            description="Index a document for search and retrieval",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the document to index"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional tags for categorization"
                    }
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="create_note",
            description="Create a new note in markdown format",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the note"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content of the note in markdown"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional tags for the note"
                    }
                },
                "required": ["title", "content"]
            }
        ),
        types.Tool(
            name="search_documents",
            description="Search indexed documents by keywords or tags",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional tags to filter results"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10)",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="extract_metadata",
            description="Extract metadata from a document",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the document"
                    }
                },
                "required": ["path"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests.
    
    Args:
        name: Name of the tool to execute
        arguments: Arguments for the tool
        
    Returns:
        List of content items with the tool result
        
    Raises:
        ValueError: If tool name is unknown
    """
    if arguments is None:
        arguments = {}
    
    try:
        if name == "index_document":
            path = arguments.get("path")
            tags = arguments.get("tags", [])
            result = await doc_processor.index_document(path, tags)
            return [types.TextContent(
                type="text",
                text=f"Document indexed successfully: {result}"
            )]
        
        elif name == "create_note":
            title = arguments.get("title")
            content = arguments.get("content")
            tags = arguments.get("tags", [])
            result = await doc_processor.create_note(title, content, tags)
            return [types.TextContent(
                type="text",
                text=f"Note created successfully at: {result}"
            )]
        
        elif name == "search_documents":
            query = arguments.get("query")
            tags = arguments.get("tags", [])
            limit = arguments.get("limit", 10)
            results = await doc_processor.search_documents(query, tags, limit)
            return [types.TextContent(
                type="text",
                text=json.dumps(results, indent=2)
            )]
        
        elif name == "extract_metadata":
            path = arguments.get("path")
            metadata = await doc_processor.extract_metadata(path)
            return [types.TextContent(
                type="text",
                text=json.dumps(metadata, indent=2)
            )]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except DocumentError as e:
        logger.error(f"Document error in {name}: {e}")
        return [types.TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]
    except Exception as e:
        logger.error(f"Unexpected error in {name}: {e}")
        return [types.TextContent(
            type="text",
            text=f"Unexpected error: {str(e)}"
        )]


async def main():
    """Main entry point for the MCP server."""
    logger.info("Starting Document Assistant MCP Server")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="document-assistant",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
