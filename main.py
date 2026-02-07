"""
Website Chatbot - Main Entry Point

A simple tool to crawl a website, extract content, and chat with it using a local LLM.
"""

import sys
from crawler import WebCrawler
from document_processor import DocumentProcessor
from data_store import DataStore
from llm_interface import LLMInterface
import os


def print_banner():
    """Display welcome banner."""
    print("\n" + "=" * 50)
    print("Website Data Chatbot - MVP")
    print("=" * 50)
    print()


def get_user_url():
    """Prompt user for a valid URL."""
    while True:
        url = input("Enter the website URL to crawl: ").strip()
        if url:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            return url
        print("Please enter a valid URL.")


def display_stats(crawler, processor):
    """Display crawling and processing statistics."""
    print(f"\n[Stats] Pages crawled: {len(crawler.visited_urls)}")
    print(f"[Stats] Text chunks created: {len(processor.chunks)}")
    print()


def main():
    """Main application flow."""
    print_banner()

    # Check if LLM is available
    print("[1/6] Checking local LLM availability...")
    llm = LLMInterface()
    if not llm.is_available():
        print("ERROR: Local LLM not available. Please install and start Ollama.")
        print("Visit: https://ollama.ai/")
        sys.exit(1)
    print("      LLM ready!")

    # Get URL from user
    url = get_user_url()

    # Initialize components
    print("\n[2/6] Initializing crawler...")
    crawler = WebCrawler(base_url=url, max_pages=50)

    print("[3/6] Crawling website (this may take a while)...")
    pages = crawler.crawl()
    print(f"      Discovered {len(pages)} pages")

    if not pages:
        print("ERROR: No pages were crawled. Please check the URL and try again.")
        sys.exit(1)

    # Process documents
    print("\n[4/6] Processing content...")
    processor = DocumentProcessor()
    all_text = ""
    for url, content in pages.items():
        all_text += content + "\n\n"

    chunks = processor.process_text(all_text, source_url=url)
    print(f"      Created {len(chunks)} text chunks")

    # Build vector store
    print("\n[5/6] Building vector store...")
    data_store = DataStore()
    data_store.add_documents(chunks)
    print("      Vector store ready!")

    # Chat loop
    print("\n[6/6] Starting chat interface...")
    print("\n" + "=" * 50)
    print("Ready! Ask questions about the website content.")
    print("Commands: 'quit' to exit, 'stats' for statistics")
    print("=" * 50 + "\n")

    while True:
        try:
            question = input("You: ").strip()

            if not question:
                continue

            if question.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break

            if question.lower() == 'stats':
                display_stats(crawler, processor)
                continue

            # Retrieve relevant context
            relevant_docs = data_store.search(question, top_k=3)
            context = "\n\n".join(relevant_docs)

            # Generate response
            print("\nBot: ", end="", flush=True)
            response = llm.generate_response(question, context)
            print(response)
            print()

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()
