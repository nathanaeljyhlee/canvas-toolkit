"""
Test Suite for Canvas Toolkit Phase 2.5: Announcements & Modules
Tests new data models, API methods, and export functionality.

Author: Claude Code (Feb 10, 2026)
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta

# Import Canvas client and models
from canvas_toolkit.client import CanvasClient
from canvas_toolkit.models import Assignment
from canvas_toolkit.models.announcement import Announcement
from canvas_toolkit.models.module import Module, ModuleItem
from canvas_toolkit.utils.html_parser import HTMLTextExtractor
from canvas_toolkit.writers import ExcelWriter, CSVWriter, JSONWriter


# Configuration
CANVAS_URL = "https://babson.instructure.com"
ENV_PATH = r"C:\Users\natha\Desktop\Babson Claude Code\secrets\Canvas API Key.env"

# Load API token
with open(ENV_PATH, 'r') as f:
    for line in f:
        if line.startswith('CANVAS_API_TOKEN='):
            API_TOKEN = line.split('=', 1)[1].strip()
            break


def test_html_parser():
    """Test HTML text extraction."""
    print("\n" + "="*80)
    print("TEST 1: HTML Parser")
    print("="*80)

    # Test plain text extraction
    html = """
    <p>This is a <strong>test</strong> announcement.</p>
    <p>Here's a link: <a href="https://example.com">Click here</a></p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
    """

    text = HTMLTextExtractor.extract(html)
    print(f"Plain text: {text}")
    assert "test announcement" in text
    assert "Click here" in text
    print("[OK] Text extraction works")

    # Test link extraction
    links = HTMLTextExtractor.extract_links(html)
    print(f"Links found: {len(links)}")
    assert len(links) == 1
    assert links[0]['url'] == "https://example.com"
    assert links[0]['text'] == "Click here"
    print("[OK] Link extraction works")


def test_announcement_model():
    """Test Announcement data model."""
    print("\n" + "="*80)
    print("TEST 2: Announcement Model")
    print("="*80)

    # Mock API response
    api_response = {
        "id": 12345,
        "title": "Week 5 Reading Assignment",
        "posted_at": "2026-02-03T14:30:00Z",
        "author": {"display_name": "Prof. Smith"},
        "html_url": "https://babson.instructure.com/courses/123/discussion_topics/12345",
        "message": "<p>Please read Chapter 5 before class. <a href='https://example.com/reading.pdf'>Download PDF</a></p>",
        "attachments": [{"filename": "syllabus.pdf"}],
        "_course_id": "123",
        "_course_name": "Business Analytics"
    }

    announcement = Announcement.from_canvas_api(api_response)

    print(f"Title: {announcement.title}")
    print(f"Posted: {announcement.posted_date_formatted}")
    print(f"Message text: {announcement.message_text}")
    print(f"Message preview: {announcement.message_preview}")
    print(f"Embedded links: {len(announcement.embedded_links)}")
    print(f"Is recent: {announcement.is_recent}")

    assert announcement.title == "Week 5 Reading Assignment"
    assert announcement.course_name == "Business Analytics"
    assert len(announcement.embedded_links) == 1
    assert "Chapter 5" in announcement.message_text
    print("[OK] Announcement model works")


def test_module_model():
    """Test Module and ModuleItem models."""
    print("\n" + "="*80)
    print("TEST 3: Module Model")
    print("="*80)

    # Mock API response
    api_response = {
        "id": 678,
        "name": "Week 1: Introduction",
        "items": [
            {
                "id": 1001,
                "module_id": 678,
                "position": 1,
                "title": "Syllabus",
                "type": "Page",
                "html_url": "https://babson.instructure.com/courses/123/pages/syllabus",
                "published": True,
                "indent": 0,
                "content_details": {}
            },
            {
                "id": 1002,
                "module_id": 678,
                "position": 2,
                "title": "Homework 1",
                "type": "Assignment",
                "html_url": "https://babson.instructure.com/courses/123/assignments/1002",
                "published": True,
                "indent": 1,
                "content_details": {
                    "due_at": "2026-02-15T23:59:00Z",
                    "points_possible": 100
                }
            }
        ],
        "_course_id": "123",
        "_course_name": "Business Analytics"
    }

    module = Module.from_canvas_api(api_response, "Business Analytics")

    print(f"Module name: {module.name}")
    print(f"Items count: {len(module.items)}")

    # Check first item
    item1 = module.items[0]
    print(f"\nItem 1: {item1.title_with_indent}")
    print(f"  Type: {item1.type}")
    print(f"  Indent: {item1.indent}")

    # Check second item (indented)
    item2 = module.items[1]
    print(f"\nItem 2: {item2.title_with_indent}")
    print(f"  Type: {item2.type}")
    print(f"  Indent: {item2.indent}")
    print(f"  Due: {item2.due_date_formatted}")

    assert module.name == "Week 1: Introduction"
    assert len(module.items) == 2
    assert item1.title_with_indent == "Syllabus"  # No indent
    assert item2.title_with_indent == "  Homework 1"  # 1 indent = 2 spaces
    assert item2.points_possible == 100
    print("[OK] Module model works")


def test_api_announcements():
    """Test announcements API integration."""
    print("\n" + "="*80)
    print("TEST 4: Announcements API")
    print("="*80)

    client = CanvasClient(CANVAS_URL, API_TOKEN)

    # Get active courses
    courses = client.get_courses()
    test_course_ids = [str(c['id']) for c in courses[:3]]  # Test with first 3 courses

    print(f"Testing with {len(test_course_ids)} courses")

    # Fetch announcements
    announcements_data = client.get_all_announcements(
        course_ids=test_course_ids,
        days_back=30
    )

    print(f"Found {len(announcements_data)} announcements")

    if announcements_data:
        # Convert to objects
        announcements = [Announcement.from_canvas_api(a) for a in announcements_data]

        # Display sample
        sample = announcements[0]
        print(f"\nSample announcement:")
        print(f"  Title: {sample.title}")
        print(f"  Course: {sample.course_name}")
        print(f"  Posted: {sample.posted_date_formatted}")
        print(f"  Preview: {sample.message_preview[:100]}...")

        print("[OK] Announcements API works")
    else:
        print("[WARN]  No announcements in last 30 days (this is OK)")


def test_api_modules():
    """Test modules API integration."""
    print("\n" + "="*80)
    print("TEST 5: Modules API")
    print("="*80)

    client = CanvasClient(CANVAS_URL, API_TOKEN)

    # Get active courses
    courses = client.get_courses()
    test_course_ids = [str(c['id']) for c in courses[:3]]

    print(f"Testing with {len(test_course_ids)} courses")

    # Fetch modules
    modules_data = client.get_all_modules(course_ids=test_course_ids)

    print(f"Found {len(modules_data)} modules")

    if modules_data:
        # Convert to Module objects and flatten to items
        all_items = []
        for mod_data in modules_data[:5]:  # Test first 5 modules
            mod = Module.from_canvas_api(
                mod_data,
                mod_data["_course_name"]
            )
            all_items.extend(mod.items)

        print(f"Total module items: {len(all_items)}")

        if all_items:
            # Display sample
            sample = all_items[0]
            print(f"\nSample module item:")
            print(f"  Title: {sample.title_with_indent}")
            print(f"  Module: {sample.module_name}")
            print(f"  Type: {sample.type}")
            print(f"  Published: {'Yes' if sample.published else 'No'}")

        print("[OK] Modules API works")
    else:
        print("[WARN]  No modules found (this might indicate an issue)")


def test_excel_export():
    """Test Excel multi-content export."""
    print("\n" + "="*80)
    print("TEST 6: Excel Multi-Content Export")
    print("="*80)

    client = CanvasClient(CANVAS_URL, API_TOKEN)

    # Get active courses
    courses = client.get_courses()
    test_course_ids = [str(c['id']) for c in courses[:2]]

    # Fetch all content types
    print("Fetching assignments...")
    assignments_data = client.get_all_assignments(course_ids=test_course_ids)
    assignments = [Assignment.from_canvas_api(a) for a in assignments_data][:10]

    print("Fetching announcements...")
    announcements_data = client.get_all_announcements(course_ids=test_course_ids, days_back=30)
    announcements = [Announcement.from_canvas_api(a) for a in announcements_data]

    print("Fetching modules...")
    modules_data = client.get_all_modules(course_ids=test_course_ids)
    all_items = []
    for mod_data in modules_data[:3]:
        mod = Module.from_canvas_api(
            mod_data,
            mod_data["_course_name"]
        )
        all_items.extend(mod.items)
    modules = all_items[:10] if all_items else None

    print(f"Content counts: {len(assignments)} assignments, {len(announcements) if announcements else 0} announcements, {len(modules) if modules else 0} modules")

    # Export to Excel
    filename = "test_phase2_5_export.xlsx"
    writer = ExcelWriter(filename)
    output_path = writer.write(
        assignments=assignments,
        announcements=announcements,
        modules=modules
    )

    print(f"[OK] Excel file created: {output_path}")
    print("   Please open the file manually to verify:")
    print("   - Check sheet count (should have 2-3 sheets)")
    print("   - Verify 'All Assignments' sheet (conditional formatting)")
    print("   - Verify 'All Announcements' sheet (recent = green)")
    print("   - Verify 'All Modules' sheet (indented titles)")
    print("   - Click Canvas links (should open in browser)")


def test_json_export():
    """Test JSON combined export."""
    print("\n" + "="*80)
    print("TEST 7: JSON Combined Export")
    print("="*80)

    client = CanvasClient(CANVAS_URL, API_TOKEN)

    # Get limited data for testing
    courses = client.get_courses()
    test_course_ids = [str(c['id']) for c in courses[:1]]

    assignments_data = client.get_all_assignments(course_ids=test_course_ids)
    assignments = [Assignment.from_canvas_api(a) for a in assignments_data][:5]

    announcements_data = client.get_all_announcements(course_ids=test_course_ids, days_back=30)
    announcements = [Announcement.from_canvas_api(a) for a in announcements_data][:5] if announcements_data else None

    # Export to JSON
    filename = "test_phase2_5_export.json"
    writer = JSONWriter(filename)
    output_path = writer.write(
        assignments=assignments,
        announcements=announcements
    )

    # Read back and validate structure
    with open(output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"JSON keys: {list(data.keys())}")
    assert "exported_at" in data
    assert "assignments" in data
    assert data["assignments"]["count"] == len(assignments)

    if announcements:
        assert "announcements" in data
        assert data["announcements"]["count"] == len(announcements)

    print(f"[OK] JSON file created: {output_path}")
    print("   Structure validated successfully")


def test_csv_export():
    """Test CSV separate files export."""
    print("\n" + "="*80)
    print("TEST 8: CSV Separate Files Export")
    print("="*80)

    client = CanvasClient(CANVAS_URL, API_TOKEN)

    # Get limited data
    courses = client.get_courses()
    test_course_ids = [str(c['id']) for c in courses[:1]]

    assignments_data = client.get_all_assignments(course_ids=test_course_ids)
    assignments = [Assignment.from_canvas_api(a) for a in assignments_data][:5]

    # Export to CSV
    filename = "test_phase2_5_assignments.csv"
    writer = CSVWriter(filename)
    writer.write(assignments)

    print(f"[OK] CSV file created: {filename}")
    print("   Open the file to verify data format")


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("CANVAS TOOLKIT PHASE 2.5 TEST SUITE")
    print("="*80)

    try:
        # Unit tests
        test_html_parser()
        test_announcement_model()
        test_module_model()

        # API integration tests
        test_api_announcements()
        test_api_modules()

        # Export tests
        test_excel_export()
        test_json_export()
        test_csv_export()

        print("\n" + "="*80)
        print("ALL TESTS PASSED [OK]")
        print("="*80)
        print("\nManual verification checklist:")
        print("[ ] Open test_phase2_5_export.xlsx")
        print("[ ] Verify sheet count and names")
        print("[ ] Check conditional formatting (assignments = red/yellow, announcements = green)")
        print("[ ] Check module items are indented")
        print("[ ] Click Canvas links (should open in browser)")
        print("[ ] Open test_phase2_5_export.json and verify structure")
        print("[ ] Open test_phase2_5_assignments.csv and verify format")

    except Exception as e:
        print(f"\n[FAIL] TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
