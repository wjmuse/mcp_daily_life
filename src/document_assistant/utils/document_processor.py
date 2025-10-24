"""Document processing utilities."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .errors import (
    DocumentNotFoundError,
    DocumentFormatError,
    DocumentIndexError,
    DocumentSearchError
)

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Handles document processing, indexing, and search operations."""
    
    def __init__(self, storage_dir: str = "./documents", index_dir: str = "./index"):
        """Initialize document processor.
        
        Args:
            storage_dir: Directory for storing documents
            index_dir: Directory for storing index data
        """
        self.storage_dir = Path(storage_dir)
        self.index_dir = Path(index_dir)
        
        # Create directories if they don't exist
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        
        # Load or create index
        self.index_file = self.index_dir / "documents.json"
        self.index = self._load_index()
    
    def _load_index(self) -> Dict[str, Any]:
        """Load document index from file.
        
        Returns:
            Document index dictionary
        """
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load index: {e}")
                return {"documents": {}, "tags": {}}
        return {"documents": {}, "tags": {}}
    
    def _save_index(self) -> None:
        """Save document index to file."""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
            raise DocumentIndexError(f"Failed to save index: {e}")
    
    async def index_document(self, path: str, tags: List[str] = None) -> str:
        """Index a document for search and retrieval.
        
        Args:
            path: Path to the document
            tags: Optional list of tags
            
        Returns:
            Document ID
            
        Raises:
            DocumentNotFoundError: If document doesn't exist
            DocumentIndexError: If indexing fails
        """
        doc_path = Path(path)
        if not doc_path.exists():
            raise DocumentNotFoundError(path)
        
        try:
            # Read document content
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate document ID
            doc_id = str(doc_path.absolute())
            
            # Extract metadata
            metadata = {
                "id": doc_id,
                "path": str(doc_path.absolute()),
                "filename": doc_path.name,
                "extension": doc_path.suffix,
                "size": doc_path.stat().st_size,
                "created": datetime.fromtimestamp(doc_path.stat().st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(doc_path.stat().st_mtime).isoformat(),
                "tags": tags or [],
                "indexed_at": datetime.now().isoformat()
            }
            
            # Store in index
            self.index["documents"][doc_id] = metadata
            
            # Update tag index
            for tag in (tags or []):
                if tag not in self.index["tags"]:
                    self.index["tags"][tag] = []
                if doc_id not in self.index["tags"][tag]:
                    self.index["tags"][tag].append(doc_id)
            
            # Save index
            self._save_index()
            
            logger.info(f"Indexed document: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Failed to index document {path}: {e}")
            raise DocumentIndexError(f"Failed to index document: {e}", path)
    
    async def create_note(self, title: str, content: str, tags: List[str] = None) -> str:
        """Create a new note in markdown format.
        
        Args:
            title: Note title
            content: Note content in markdown
            tags: Optional list of tags
            
        Returns:
            Path to created note
        """
        # Generate filename from title
        filename = title.lower().replace(" ", "-") + ".md"
        note_path = self.storage_dir / filename
        
        # Create note content with frontmatter
        timestamp = datetime.now().isoformat()
        frontmatter = f"""---
title: {title}
created: {timestamp}
tags: {', '.join(tags or [])}
---

"""
        note_content = frontmatter + content
        
        try:
            # Write note
            with open(note_path, 'w', encoding='utf-8') as f:
                f.write(note_content)
            
            # Index the note
            await self.index_document(str(note_path), tags)
            
            logger.info(f"Created note: {note_path}")
            return str(note_path)
            
        except Exception as e:
            logger.error(f"Failed to create note: {e}")
            raise DocumentIndexError(f"Failed to create note: {e}")
    
    async def search_documents(
        self, 
        query: str, 
        tags: List[str] = None, 
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search indexed documents.
        
        Args:
            query: Search query string
            tags: Optional tags to filter by
            limit: Maximum number of results
            
        Returns:
            List of matching documents with metadata
        """
        try:
            results = []
            query_lower = query.lower()
            
            for doc_id, metadata in self.index["documents"].items():
                # Check tag filter
                if tags:
                    doc_tags = set(metadata.get("tags", []))
                    if not doc_tags.intersection(set(tags)):
                        continue
                
                # Simple search in filename and tags
                filename_lower = metadata.get("filename", "").lower()
                doc_tags_str = " ".join(metadata.get("tags", [])).lower()
                
                if query_lower in filename_lower or query_lower in doc_tags_str:
                    results.append(metadata)
                
                if len(results) >= limit:
                    break
            
            logger.info(f"Search for '{query}' returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise DocumentSearchError(f"Search failed: {e}", query)
    
    async def extract_metadata(self, path: str) -> Dict[str, Any]:
        """Extract metadata from a document.
        
        Args:
            path: Path to the document
            
        Returns:
            Document metadata
            
        Raises:
            DocumentNotFoundError: If document doesn't exist
        """
        doc_path = Path(path)
        if not doc_path.exists():
            raise DocumentNotFoundError(path)
        
        try:
            # Check if already indexed
            doc_id = str(doc_path.absolute())
            if doc_id in self.index["documents"]:
                return self.index["documents"][doc_id]
            
            # Extract basic metadata
            metadata = {
                "path": str(doc_path.absolute()),
                "filename": doc_path.name,
                "extension": doc_path.suffix,
                "size": doc_path.stat().st_size,
                "created": datetime.fromtimestamp(doc_path.stat().st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(doc_path.stat().st_mtime).isoformat()
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to extract metadata from {path}: {e}")
            raise DocumentFormatError(f"Failed to extract metadata: {e}", path)
