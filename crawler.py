"""
Web Crawler Module

Handles crawling websites and extracting HTML content.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from typing import Dict, Set


class WebCrawler:
    """Simple web crawler that respects rate limits and domain boundaries."""

    def __init__(self, base_url: str, max_pages: int = 50, delay: float = 0.5):
        """
        Initialize the crawler.

        Args:
            base_url: Starting URL to crawl
            max_pages: Maximum number of pages to crawl
            delay: Delay between requests in seconds
        """
        self.base_url = base_url
        self.max_pages = max_pages
        self.delay = delay
        self.visited_urls: Set[str] = set()
        self.domain = urlparse(base_url).netloc

        # Headers to identify as a bot
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; WebsiteChatbot/1.0)'
        }

    def is_valid_url(self, url: str) -> bool:
        """
        Check if URL should be crawled.

        Args:
            url: URL to validate

        Returns:
            True if URL is valid and should be crawled
        """
        parsed = urlparse(url)

        # Must be same domain
        if parsed.netloc != self.domain:
            return False

        # Skip common non-content URLs
        skip_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip',
                          '.exe', '.dmg', '.mp4', '.mp3', '.css', '.js')
        if parsed.path.lower().endswith(skip_extensions):
            return False

        return True

    def extract_links(self, html: str, current_url: str) -> Set[str]:
        """
        Extract all valid links from HTML content.

        Args:
            html: HTML content
            current_url: Current page URL for resolving relative links

        Returns:
            Set of absolute URLs
        """
        soup = BeautifulSoup(html, 'html.parser')
        links = set()

        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            # Resolve relative URLs
            absolute_url = urljoin(current_url, href)
            # Remove fragments
            absolute_url = absolute_url.split('#')[0]

            if self.is_valid_url(absolute_url):
                links.add(absolute_url)

        return links

    def extract_text(self, html: str) -> str:
        """
        Extract clean text from HTML.

        Args:
            html: HTML content

        Returns:
            Cleaned text content
        """
        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style elements
        for script in soup(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()

        # Get text
        text = soup.get_text(separator=' ')

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text

    def fetch_page(self, url: str) -> tuple[str, str]:
        """
        Fetch a page and extract its content.

        Args:
            url: URL to fetch

        Returns:
            Tuple of (html, text_content)
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            html = response.text
            text = self.extract_text(html)

            return html, text

        except Exception as e:
            print(f"      Error fetching {url}: {e}")
            return "", ""

    def crawl(self) -> Dict[str, str]:
        """
        Crawl the website starting from base_url.

        Returns:
            Dictionary mapping URLs to their text content
        """
        to_visit = {self.base_url}
        pages_content = {}

        while to_visit and len(self.visited_urls) < self.max_pages:
            url = to_visit.pop()

            if url in self.visited_urls:
                continue

            print(f"      Crawling [{len(self.visited_urls) + 1}/{self.max_pages}]: {url[:60]}...")

            html, text = self.fetch_page(url)

            if text:
                self.visited_urls.add(url)
                pages_content[url] = text

                # Extract and queue new links
                new_links = self.extract_links(html, url)
                to_visit.update(new_links - self.visited_urls)

            # Be polite - delay between requests
            time.sleep(self.delay)

        return pages_content
