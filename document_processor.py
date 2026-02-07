"""
Document Processor Module

Handles text chunking and processing for LLM consumption.
"""

from typing import List, Dict


class DocumentProcessor:
    """Process and chunk text documents for vector storage."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document processor.

        Args:
            chunk_size: Target size for each text chunk (in characters)
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.chunks: List[Dict[str, str]] = []

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks.

        Args:
            text: Text to chunk

        Returns:
            List of text chunks
        """
        if len(text) <= self.chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            # Get chunk
            end = start + self.chunk_size
            chunk = text[start:end]

            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings
                last_period = chunk.rfind('. ')
                last_question = chunk.rfind('? ')
                last_exclamation = chunk.rfind('! ')

                break_point = max(last_period, last_question, last_exclamation)

                if break_point > self.chunk_size // 2:  # Only break if in latter half
                    chunk = chunk[:break_point + 2]
                    end = start + break_point + 2

            chunks.append(chunk.strip())

            # Move start position with overlap
            start = end - self.chunk_overlap

            # Avoid infinite loop
            if start <= 0 or end >= len(text):
                break

        return chunks

    def process_text(self, text: str, source_url: str = "") -> List[Dict[str, str]]:
        """
        Process text into chunks with metadata.

        Args:
            text: Text to process
            source_url: Source URL for metadata

        Returns:
            List of chunk dictionaries with text and metadata
        """
        chunks = self.chunk_text(text)

        processed_chunks = []
        for i, chunk in enumerate(chunks):
            if chunk.strip():  # Skip empty chunks
                chunk_data = {
                    'text': chunk,
                    'source': source_url,
                    'chunk_id': i
                }
                processed_chunks.append(chunk_data)

        self.chunks.extend(processed_chunks)
        return processed_chunks

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text.

        Args:
            text: Text to clean

        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = ' '.join(text.split())

        # Remove very short fragments
        if len(text) < 50:
            return ""

        return text
