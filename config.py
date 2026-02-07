"""
Configuration Settings

Central configuration for the website chatbot.
"""

# Crawler settings
MAX_PAGES = 50
CRAWL_DELAY = 0.5  # seconds between requests

# Document processing
CHUNK_SIZE = 1000  # characters
CHUNK_OVERLAP = 200  # characters

# LLM settings
OLLAMA_MODEL = "llama3.2"  # Change to your preferred Ollama model
OLLAMA_BASE_URL = "http://localhost:11434"

# Vector store
VECTOR_STORE_PATH = "./data/vectorstore"

# Search settings
TOP_K_RESULTS = 3  # Number of context chunks to retrieve
