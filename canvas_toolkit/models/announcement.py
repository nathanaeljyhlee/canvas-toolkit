"""Announcement data model."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

from canvas_toolkit.utils.html_parser import HTMLTextExtractor


@dataclass
class Announcement:
    """Standardized announcement data model."""

    id: str
    title: str
    course_id: str
    course_name: str
    posted_at: Optional[str]
    author: str
    html_url: str
    message_html: Optional[str] = None
    message_text: Optional[str] = None
    embedded_links: list = field(default_factory=list)
    attachments: list = field(default_factory=list)

    @classmethod
    def from_canvas_api(cls, api_response: Dict[str, Any]) -> "Announcement":
        """
        Create Announcement from Canvas API response.

        Args:
            api_response: Raw announcement dict from Canvas API

        Returns:
            Announcement instance
        """
        # Extract HTML message
        message_html = api_response.get("message", "")

        # Parse HTML to plain text and extract links
        message_text = None
        embedded_links = []
        if message_html:
            message_text = HTMLTextExtractor.extract(message_html)
            embedded_links = HTMLTextExtractor.extract_links(message_html)

        # Get author name
        author_data = api_response.get("author", {})
        author = author_data.get("display_name", "Unknown") if isinstance(author_data, dict) else "Unknown"

        return cls(
            id=str(api_response["id"]),
            title=api_response.get("title", "Untitled Announcement"),
            course_id=str(api_response.get("_course_id", "")),
            course_name=api_response.get("_course_name", "Unknown Course"),
            posted_at=api_response.get("posted_at"),
            author=author,
            html_url=api_response.get("html_url", ""),
            message_html=message_html,
            message_text=message_text,
            embedded_links=embedded_links,
            attachments=api_response.get("attachments", []),
        )

    @property
    def posted_date_formatted(self) -> str:
        """Return formatted posted date or 'Unknown'."""
        if not self.posted_at:
            return "Unknown"
        try:
            dt = datetime.fromisoformat(self.posted_at.replace('Z', '+00:00'))
            return dt.strftime("%m/%d/%Y %I:%M %p")
        except (ValueError, AttributeError):
            return self.posted_at

    @property
    def message_preview(self) -> str:
        """Return first 500 characters of message text."""
        if not self.message_text:
            return ""
        return self.message_text[:500]

    @property
    def is_recent(self) -> bool:
        """Check if announcement was posted in the last 7 days."""
        if not self.posted_at:
            return False
        try:
            posted_date = datetime.fromisoformat(self.posted_at.replace('Z', '+00:00'))
            cutoff_date = datetime.now(posted_date.tzinfo) - timedelta(days=7)
            return posted_date > cutoff_date
        except (ValueError, AttributeError):
            return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for export."""
        return {
            "Course": self.course_name,
            "Title": self.title,
            "Posted Date": self.posted_date_formatted,
            "Author": self.author,
            "Message Preview": self.message_preview,
            "Embedded Links": len(self.embedded_links),
            "Attachments": len(self.attachments),
            "Canvas Link": self.html_url,
            "Canvas ID": self.id,
        }
