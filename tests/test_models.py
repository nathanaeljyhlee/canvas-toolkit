"""Tests for data models."""

import pytest
from datetime import datetime, timedelta
from canvas_toolkit.models.announcement import Announcement
from canvas_toolkit.models.module import Module, ModuleItem
from canvas_toolkit.models import Assignment


class TestAnnouncement:
    """Test suite for Announcement model."""

    def test_from_canvas_api_basic(self):
        """Test creating announcement from basic API response."""
        api_data = {
            "id": 123,
            "title": "Test Announcement",
            "_course_id": "456",
            "_course_name": "Test Course",
            "posted_at": "2026-02-10T10:00:00Z",
            "author": {"display_name": "Professor Smith"},
            "html_url": "https://canvas.instructure.com/courses/456/discussion_topics/123",
            "message": "<p>Test message</p>"
        }
        announcement = Announcement.from_canvas_api(api_data)

        assert announcement.id == "123"
        assert announcement.title == "Test Announcement"
        assert announcement.course_id == "456"
        assert announcement.course_name == "Test Course"
        assert announcement.author == "Professor Smith"
        assert "Test message" in announcement.message_text

    def test_missing_optional_fields(self):
        """Test handling missing optional fields."""
        api_data = {
            "id": 123,
            "_course_id": "456",
            "_course_name": "Test Course"
        }
        announcement = Announcement.from_canvas_api(api_data)

        assert announcement.title == "Untitled Announcement"
        assert announcement.posted_at is None
        assert announcement.author == "Unknown"
        assert announcement.message_text is None

    def test_posted_date_formatting(self):
        """Test posted date formatting."""
        api_data = {
            "id": 123,
            "posted_at": "2026-02-10T14:30:00Z",
            "_course_id": "456",
            "_course_name": "Test Course"
        }
        announcement = Announcement.from_canvas_api(api_data)
        formatted = announcement.posted_date_formatted

        assert "02/10/2026" in formatted
        # Should include time
        assert ":" in formatted

    def test_invalid_date_format(self):
        """Test handling of invalid date format."""
        api_data = {
            "id": 123,
            "posted_at": "invalid-date",
            "_course_id": "456",
            "_course_name": "Test Course"
        }
        announcement = Announcement.from_canvas_api(api_data)

        # Should return the raw string instead of crashing
        assert announcement.posted_date_formatted == "invalid-date"

    def test_none_posted_date(self):
        """Test handling of None posted date."""
        api_data = {
            "id": 123,
            "posted_at": None,
            "_course_id": "456",
            "_course_name": "Test Course"
        }
        announcement = Announcement.from_canvas_api(api_data)

        assert announcement.posted_date_formatted == "Unknown"
        assert announcement.is_recent is False

    def test_is_recent_check(self):
        """Test is_recent property for recent announcements."""
        # Create announcement from 3 days ago
        recent_date = (datetime.now() - timedelta(days=3)).isoformat() + "Z"
        api_data = {
            "id": 123,
            "posted_at": recent_date,
            "_course_id": "456",
            "_course_name": "Test Course"
        }
        announcement = Announcement.from_canvas_api(api_data)
        assert announcement.is_recent is True

        # Create announcement from 10 days ago
        old_date = (datetime.now() - timedelta(days=10)).isoformat() + "Z"
        api_data["posted_at"] = old_date
        announcement = Announcement.from_canvas_api(api_data)
        assert announcement.is_recent is False

    def test_message_preview_truncation(self):
        """Test that long messages are truncated in preview."""
        long_message = "A" * 600  # 600 characters
        api_data = {
            "id": 123,
            "message": f"<p>{long_message}</p>",
            "_course_id": "456",
            "_course_name": "Test Course"
        }
        announcement = Announcement.from_canvas_api(api_data)

        assert len(announcement.message_preview) == 500
        assert announcement.message_preview == "A" * 500

    def test_html_link_extraction(self):
        """Test extracting embedded links from HTML message."""
        api_data = {
            "id": 123,
            "message": '<p>Check <a href="https://example.com">this link</a> out</p>',
            "_course_id": "456",
            "_course_name": "Test Course"
        }
        announcement = Announcement.from_canvas_api(api_data)

        assert len(announcement.embedded_links) == 1
        assert announcement.embedded_links[0]["url"] == "https://example.com"

    def test_to_dict_export(self):
        """Test converting announcement to dict for export."""
        api_data = {
            "id": 123,
            "title": "Test",
            "posted_at": "2026-02-10T10:00:00Z",
            "author": {"display_name": "Prof"},
            "html_url": "https://example.com",
            "message": "<p>Test</p>",
            "_course_id": "456",
            "_course_name": "Test Course"
        }
        announcement = Announcement.from_canvas_api(api_data)
        export_dict = announcement.to_dict()

        assert "Course" in export_dict
        assert "Title" in export_dict
        assert "Posted Date" in export_dict
        assert export_dict["Course"] == "Test Course"


class TestModuleItem:
    """Test suite for ModuleItem model."""

    def test_from_canvas_api_basic(self):
        """Test creating module item from API response."""
        api_data = {
            "id": 789,
            "module_id": 456,
            "position": 1,
            "title": "Week 1 Reading",
            "type": "Page",
            "html_url": "https://canvas.instructure.com/courses/123/pages/week-1",
            "published": True
        }
        item = ModuleItem.from_canvas_api(
            api_response=api_data,
            module_name="Module 1",
            course_id="123",
            course_name="Test Course"
        )

        assert item.id == "789"
        assert item.title == "Week 1 Reading"
        assert item.type == "Page"
        assert item.published is True

    def test_indent_formatting(self):
        """Test title indentation."""
        api_data = {
            "id": 789,
            "title": "Nested Item",
            "indent": 2,
            "type": "Page",
            "html_url": "https://example.com"
        }
        item = ModuleItem.from_canvas_api(
            api_response=api_data,
            module_name="Module 1",
            course_id="123",
            course_name="Test Course"
        )

        # Should have 4 spaces (2 spaces per indent level)
        assert item.title_with_indent == "    Nested Item"

    def test_no_due_date(self):
        """Test handling of items without due dates."""
        api_data = {
            "id": 789,
            "title": "Reading",
            "type": "Page",
            "html_url": "https://example.com"
        }
        item = ModuleItem.from_canvas_api(
            api_response=api_data,
            module_name="Module 1",
            course_id="123",
            course_name="Test Course"
        )

        assert item.due_at is None
        assert item.due_date_formatted == "No due date"

    def test_with_due_date(self):
        """Test handling of items with due dates."""
        api_data = {
            "id": 789,
            "title": "Assignment",
            "type": "Assignment",
            "html_url": "https://example.com",
            "content_details": {
                "due_at": "2026-02-15T23:59:00Z",
                "points_possible": 100
            }
        }
        item = ModuleItem.from_canvas_api(
            api_response=api_data,
            module_name="Module 1",
            course_id="123",
            course_name="Test Course"
        )

        assert item.due_at == "2026-02-15T23:59:00Z"
        assert "02/15/2026" in item.due_date_formatted
        assert item.points_possible == 100

    def test_to_dict_export(self):
        """Test converting module item to dict for export."""
        api_data = {
            "id": 789,
            "title": "Test Item",
            "type": "Page",
            "html_url": "https://example.com",
            "published": True
        }
        item = ModuleItem.from_canvas_api(
            api_response=api_data,
            module_name="Module 1",
            course_id="123",
            course_name="Test Course"
        )
        export_dict = item.to_dict()

        assert "Course" in export_dict
        assert "Module" in export_dict
        assert "Item Title" in export_dict
        assert export_dict["Course"] == "Test Course"


class TestModule:
    """Test suite for Module model."""

    def test_from_canvas_api_with_items(self):
        """Test creating module with nested items."""
        api_data = {
            "id": 456,
            "name": "Week 1",
            "_course_id": "123",
            "items": [
                {
                    "id": 789,
                    "title": "Reading 1",
                    "type": "Page",
                    "html_url": "https://example.com",
                    "published": True
                },
                {
                    "id": 790,
                    "title": "Reading 2",
                    "type": "Page",
                    "html_url": "https://example.com",
                    "published": True
                }
            ]
        }
        module = Module.from_canvas_api(api_data, course_name="Test Course")

        assert module.id == "456"
        assert module.name == "Week 1"
        assert len(module.items) == 2
        assert module.items[0].title == "Reading 1"

    def test_malformed_items_skipped(self):
        """Test that malformed items are skipped without crashing."""
        api_data = {
            "id": 456,
            "name": "Week 1",
            "_course_id": "123",
            "items": [
                {
                    "id": 789,
                    "title": "Valid Item",
                    "type": "Page",
                    "html_url": "https://example.com"
                },
                {
                    # Missing required 'id' field
                    "title": "Invalid Item"
                }
            ]
        }
        module = Module.from_canvas_api(api_data, course_name="Test Course")

        # Should only include the valid item
        assert len(module.items) == 1
        assert module.items[0].title == "Valid Item"

    def test_empty_items_list(self):
        """Test module with no items."""
        api_data = {
            "id": 456,
            "name": "Empty Module",
            "_course_id": "123",
            "items": []
        }
        module = Module.from_canvas_api(api_data, course_name="Test Course")

        assert len(module.items) == 0


class TestAssignment:
    """Test suite for Assignment model edge cases."""

    def test_assignment_with_null_due_date(self):
        """Test that assignments without due dates are handled."""
        api_data = {
            "id": 123,
            "name": "No Due Date Assignment",
            "due_at": None,
            "points_possible": 50,
            "html_url": "https://example.com",
            "_course_id": "456",
            "_course_name": "Test Course"
        }
        assignment = Assignment.from_canvas_api(api_data)

        assert assignment.due_at is None
        assert assignment.due_date_formatted == "No due date"
        assert assignment.is_overdue is False

    def test_assignment_with_invalid_date(self):
        """Test handling of malformed due dates."""
        api_data = {
            "id": 123,
            "name": "Invalid Date Assignment",
            "due_at": "not-a-date",
            "points_possible": 50,
            "html_url": "https://example.com",
            "_course_id": "456",
            "_course_name": "Test Course"
        }
        assignment = Assignment.from_canvas_api(api_data)

        # Should return the raw string instead of crashing
        assert assignment.due_date_formatted == "not-a-date"
