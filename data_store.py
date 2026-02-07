"""
Data Store Module

Handles vector storage and semantic search using ChromaDB.
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict
import os


class DataStore:
    """Vector store for semantic search over document chunks."""

    def __init__(self, persist_directory: str = "./data/vectorstore"):
        """
        Initialize the vector store.

        Args:
            persist_directory: Directory to persist vector data
        """
        self.persist_directory = persist_directory

        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)

        # Initialize ChromaDB client
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))

        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="website_content",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, chunks: List[Dict[str, str]]):
        """
        Add document chunks to the vector store.

        Args:
            chunks: List of chunk dictionaries with 'text' and metadata
        """
        if not chunks:
            return

        # Prepare data for ChromaDB
        documents = []
        metadatas = []
        ids = []

        for i, chunk in enumerate(chunks):
            documents.append(chunk['text'])
            metadatas.append({
                'source': chunk.get('source', ''),
                'chunk_id': chunk.get('chunk_id', i)
            })
            ids.append(f"chunk_{i}")

        # Add to collection
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query: str, top_k: int = 3) -> List[str]:
        """
        Search for relevant document chunks.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of relevant text chunks
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )

        # Extract documents from results
        if results['documents']:
            return results['documents'][0]

        return []

    def clear(self):
        """Clear all documents from the vector store."""
        self.client.delete_collection("website_content")
        self.collection = self.client.create_collection(
            name="website_content",
            metadata={"hnsw:space": "cosine"}
        )
