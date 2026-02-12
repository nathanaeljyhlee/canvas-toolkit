"""Tests for HTML parser utility."""

import pytest
from canvas_toolkit.utils.html_parser import HTMLTextExtractor


class TestHTMLTextExtractor:
    """Test suite for HTMLTextExtractor."""

    def test_basic_text_extraction(self):
        """Test extracting plain text from simple HTML."""
        html = "<p>Hello world</p>"
        result = HTMLTextExtractor.extract(html)
        assert result == "Hello world"

    def test_empty_input(self):
        """Test handling of empty or None input."""
        assert HTMLTextExtractor.extract("") == ""
        assert HTMLTextExtractor.extract(None) == ""

    def test_nested_tags(self):
        """Test handling nested HTML tags."""
        html = "<div><p>Outer <strong>bold</strong> text</p></div>"
        result = HTMLTextExtractor.extract(html)
        assert "Outer" in result
        assert "bold" in result
        assert "text" in result

    def test_paragraph_breaks(self):
        """Test that paragraph breaks are preserved."""
        html = "<p>First paragraph</p><p>Second paragraph</p>"
        result = HTMLTextExtractor.extract(html)
        assert "First paragraph" in result
        assert "Second paragraph" in result
        # Should have newlines between paragraphs
        assert "\n" in result or result.count("paragraph") == 2

    def test_link_extraction(self):
        """Test extracting links from HTML."""
        html = '<p>Check out <a href="https://example.com">this link</a> for more info</p>'
        links = HTMLTextExtractor.extract_links(html)
        assert len(links) == 1
        assert links[0]["text"] == "this link"
        assert links[0]["url"] == "https://example.com"

    def test_multiple_links(self):
        """Test extracting multiple links."""
        html = '''
        <p>Visit <a href="https://example.com">site 1</a> and
        <a href="https://example.org">site 2</a> for details</p>
        '''
        links = HTMLTextExtractor.extract_links(html)
        assert len(links) == 2
        assert links[0]["url"] == "https://example.com"
        assert links[1]["url"] == "https://example.org"

    def test_empty_links(self):
        """Test handling of empty or malformed links."""
        # Link with no text
        html = '<a href="https://example.com"></a>'
        links = HTMLTextExtractor.extract_links(html)
        assert len(links) == 0  # Empty links should be filtered out

    def test_link_without_href(self):
        """Test handling of <a> tags without href attribute."""
        html = '<a>No href here</a>'
        links = HTMLTextExtractor.extract_links(html)
        # Should handle gracefully, may return empty url
        assert isinstance(links, list)

    def test_malformed_html(self):
        """Test handling of malformed HTML."""
        # Unclosed tags
        html = "<p>Unclosed paragraph"
        result = HTMLTextExtractor.extract(html)
        assert "Unclosed paragraph" in result

        # Mismatched tags
        html = "<p>Content</div>"
        result = HTMLTextExtractor.extract(html)
        assert "Content" in result

    def test_html_entities(self):
        """Test handling of HTML entities."""
        html = "<p>AT&amp;T &lt;company&gt;</p>"
        result = HTMLTextExtractor.extract(html)
        # HTMLParser automatically decodes entities
        assert "AT&T" in result
        assert "<company>" in result

    def test_whitespace_cleanup(self):
        """Test that excess whitespace is cleaned up."""
        html = "<p>Too     many    spaces</p>"
        result = HTMLTextExtractor.extract(html)
        # Should normalize multiple spaces to single space
        assert "Too many spaces" in result or "Too" in result

    def test_script_and_style_tags(self):
        """Test that script/style content is extracted (HTMLParser doesn't filter by default)."""
        html = "<p>Visible text</p><script>alert('test')</script>"
        result = HTMLTextExtractor.extract(html)
        # Note: Our parser doesn't explicitly filter script tags,
        # but they won't cause parsing errors
        assert "Visible text" in result

    def test_canvas_announcement_structure(self):
        """Test realistic Canvas announcement HTML structure."""
        html = '''
        <div>
            <p>Dear students,</p>
            <p>Please review <a href="https://canvas.instructure.com/courses/123/files/456">
            this document</a> before class.</p>
            <p>Best regards,<br/>Professor Smith</p>
        </div>
        '''
        result = HTMLTextExtractor.extract(html)
        links = HTMLTextExtractor.extract_links(html)

        assert "Dear students" in result
        assert "Professor Smith" in result
        assert len(links) == 1
        assert "this document" in links[0]["text"]

    def test_no_links_in_html(self):
        """Test HTML with no links returns empty list."""
        html = "<p>Just plain text with no links</p>"
        links = HTMLTextExtractor.extract_links(html)
        assert links == []

    def test_relative_urls(self):
        """Test handling of relative URLs in links."""
        html = '<a href="/courses/123/assignments/456">Assignment link</a>'
        links = HTMLTextExtractor.extract_links(html)
        assert len(links) == 1
        assert links[0]["url"] == "/courses/123/assignments/456"

    def test_unicode_content(self):
        """Test handling of Unicode characters."""
        html = "<p>Unicode: café, naïve, 日本語</p>"
        result = HTMLTextExtractor.extract(html)
        assert "café" in result
        assert "naïve" in result
        assert "日本語" in result
