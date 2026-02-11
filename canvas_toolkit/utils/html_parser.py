"""HTML text extraction utilities."""

from html.parser import HTMLParser
from typing import List, Dict
import re


class HTMLTextExtractor(HTMLParser):
    """
    Extract plain text and links from HTML content.

    Provides static methods for converting HTML to plain text while preserving
    paragraph breaks and extracting embedded hyperlinks.
    """

    def __init__(self):
        """Initialize the parser."""
        super().__init__()
        self.text_parts = []
        self.links = []
        self.in_link = False
        self.current_link_url = None
        self.current_link_text = []

    def handle_starttag(self, tag, attrs):
        """Handle opening HTML tags."""
        if tag == 'a':
            self.in_link = True
            attrs_dict = dict(attrs)
            self.current_link_url = attrs_dict.get('href', '')
            self.current_link_text = []
        elif tag in ['p', 'br', 'div']:
            self.text_parts.append('\n')

    def handle_endtag(self, tag):
        """Handle closing HTML tags."""
        if tag == 'a':
            if self.current_link_url and self.current_link_text:
                link_text = ''.join(self.current_link_text).strip()
                if link_text:
                    self.links.append({
                        'text': link_text,
                        'url': self.current_link_url
                    })
            self.in_link = False
            self.current_link_url = None
            self.current_link_text = []

    def handle_data(self, data):
        """Handle text data within HTML tags."""
        clean = data.strip()
        if clean:
            self.text_parts.append(clean + ' ')
            if self.in_link:
                self.current_link_text.append(clean)

    def get_text(self) -> str:
        """
        Get cleaned plain text from parsed HTML.

        Returns:
            Plain text with preserved paragraph breaks and cleaned whitespace
        """
        text = ''.join(self.text_parts)
        # Clean up extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s+', '\n', text)
        return text.strip()

    def get_links(self) -> List[Dict[str, str]]:
        """
        Get list of extracted links.

        Returns:
            List of dicts with 'text' and 'url' keys
        """
        return self.links

    @staticmethod
    def extract(html: str) -> str:
        """
        Extract plain text from HTML.

        Converts HTML to plain text while preserving paragraph breaks
        and removing all HTML tags.

        Args:
            html: HTML string to parse

        Returns:
            Plain text extracted from HTML
        """
        if not html:
            return ""

        parser = HTMLTextExtractor()
        parser.feed(html)
        return parser.get_text()

    @staticmethod
    def extract_links(html: str) -> List[Dict[str, str]]:
        """
        Extract all hyperlinks from HTML.

        Args:
            html: HTML string to parse

        Returns:
            List of dicts with 'text' and 'url' keys for each <a> tag
        """
        if not html:
            return []

        parser = HTMLTextExtractor()
        parser.feed(html)
        return parser.get_links()
