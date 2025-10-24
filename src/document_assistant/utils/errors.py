"""Custom exceptions for document processing."""


class DocumentError(Exception):
    """Base exception for document processing errors."""
    
    def __init__(self, message: str, path: str = None):
        """Initialize document error.
        
        Args:
            message: Error message
            path: Optional path to the document that caused the error
        """
        self.message = message
        self.path = path
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """String representation of the error."""
        if self.path:
            return f"{self.message} (path: {self.path})"
        return self.message


class DocumentNotFoundError(DocumentError):
    """Exception raised when a document is not found."""
    
    def __init__(self, path: str):
        """Initialize document not found error.
        
        Args:
            path: Path to the missing document
        """
        super().__init__(f"Document not found", path)


class DocumentFormatError(DocumentError):
    """Exception raised when a document format is invalid or unsupported."""
    
    def __init__(self, message: str, path: str = None):
        """Initialize document format error.
        
        Args:
            message: Error message
            path: Optional path to the document
        """
        super().__init__(f"Format error: {message}", path)


class DocumentIndexError(DocumentError):
    """Exception raised when document indexing fails."""
    
    def __init__(self, message: str, path: str = None):
        """Initialize document index error.
        
        Args:
            message: Error message
            path: Optional path to the document
        """
        super().__init__(f"Indexing error: {message}", path)


class DocumentSearchError(DocumentError):
    """Exception raised when document search fails."""
    
    def __init__(self, message: str, query: str = None):
        """Initialize document search error.
        
        Args:
            message: Error message
            query: Optional search query that failed
        """
        self.query = query
        super().__init__(f"Search error: {message}")
    
    def __str__(self) -> str:
        """String representation of the error."""
        if self.query:
            return f"{self.message} (query: {self.query})"
        return self.message
