# Website Chatbot - MVP

A minimal viable product that crawls websites, extracts content, and enables conversational Q&A using a local LLM.

The goal was to create a RAG with all the tools at our disposal in less than an hour and a hald. In our case, we used Claude Code.

## Group Members

Ryan NAIDJI

Abdelkrim Innouche

Giuliano Zerach


## Features

- Web crawling with automatic link discovery
- Text extraction from HTML pages
- Intelligent text chunking with overlap
- Vector-based semantic search using ChromaDB
- Local LLM integration via Ollama
- Simple command-line interface

## Prerequisites

1. **Python 3.8+** - Make sure Python is installed
2. **Ollama** - Local LLM runtime

### Installing Ollama

1. Visit [https://ollama.ai/](https://ollama.ai/) and download Ollama for your system
2. Install and start Ollama
3. Pull a model (recommended: llama3.2):
   ```bash
   ollama pull llama3.2
   ```

## Installation

1. **Clone or navigate to the project directory**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Ollama is running:**
   ```bash
   ollama list
   ```
   You should see your installed models.

## Usage

1. **Start the chatbot:**
   ```bash
   python main.py
   ```

2. **Enter a website URL when prompted:**
   ```
   Enter the website URL to crawl: https://example.com
   ```

3. **Wait for crawling and processing to complete**
   - The tool will crawl up to 50 pages (configurable)
   - Text will be extracted and chunked
   - A vector store will be built for semantic search

4. **Ask questions about the website content:**
   ```
   You: What is this website about?
   Bot: [Response based on crawled content]
   ```

5. **Available commands:**
   - Type your question to get an answer
   - Type `stats` to see crawling statistics
   - Type `quit` or `exit` to exit

## Configuration

Edit `config.py` to customize:

- `MAX_PAGES` - Maximum pages to crawl (default: 50)
- `CRAWL_DELAY` - Delay between requests in seconds (default: 0.5)
- `CHUNK_SIZE` - Text chunk size in characters (default: 1000)
- `OLLAMA_MODEL` - Ollama model to use (default: "llama3.2")
- `TOP_K_RESULTS` - Number of context chunks for LLM (default: 3)

## Project Structure

```
website_chatbot/
├── main.py                 # Main entry point
├── crawler.py              # Web crawling logic
├── document_processor.py   # Text processing and chunking
├── data_store.py           # Vector storage with ChromaDB
├── llm_interface.py        # Ollama LLM integration
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── data/                  # Generated data directory
    └── vectorstore/       # Vector embeddings storage
```

## How It Works

1. **Crawling**: The crawler starts from your provided URL and follows links within the same domain, respecting rate limits and avoiding duplicate pages.

2. **Processing**: HTML content is cleaned and split into overlapping chunks suitable for the LLM's context window.

3. **Indexing**: Text chunks are converted to vector embeddings and stored in ChromaDB for semantic search.

4. **Chat**: When you ask a question:
   - The question is used to search the vector store
   - Relevant text chunks are retrieved
   - The LLM generates a response using the retrieved context

## Troubleshooting

### "Local LLM not available"
- Ensure Ollama is running: `ollama list`
- Check if Ollama is on the default port (11434)
- Try: `ollama serve`

### "No pages were crawled"
- Check the URL is accessible in your browser
- Some sites may block automated crawlers
- Check your internet connection

### ChromaDB errors
- Delete the `data/vectorstore` directory and try again
- Ensure you have write permissions in the project directory

### Slow performance
- Reduce `MAX_PAGES` in `config.py`
- Use a smaller/faster Ollama model
- Reduce `TOP_K_RESULTS` to retrieve fewer context chunks

## Limitations (MVP)

- HTML pages only (no PDF, DOCX, etc.)
- Single domain crawling
- No authentication support
- Basic error handling
- No conversation history
- No persistent storage between runs

## Future Enhancements

- Support for PDF and other document types
- Multi-domain crawling
- Persistent conversation history
- Web UI interface
- Better error recovery
- Incremental crawling/updates
- Authentication support

## License

MIT License - Feel free to use and modify as needed.

## Contributing

This is an MVP. Contributions for improvements are welcome!
