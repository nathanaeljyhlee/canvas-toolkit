#!/usr/bin/env python3
"""
Basic example: Export all assignments to Excel using Python API
(Alternative to Streamlit GUI for automation/scripting)
"""

from canvas_toolkit.client import CanvasClient
from canvas_toolkit.models import Assignment
from canvas_toolkit.writers import ExcelWriter

# Configuration
CANVAS_URL = "https://babson.instructure.com"
API_TOKEN = "your_token_here"  # Replace with your token

def main():
    # Initialize client
    print("Connecting to Canvas...")
    client = CanvasClient(CANVAS_URL, API_TOKEN)

    # Test connection
    try:
        client.test_connection()
        print("✅ Connected!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    # Fetch courses
    print("\nFetching courses...")
    courses = client.get_courses()
    print(f"Found {len(courses)} courses:")
    for course in courses:
        print(f"  - {course['name']}")

    # Fetch all assignments
    print("\nFetching assignments...")
    assignments_data = client.get_all_assignments()

    # Convert to Assignment objects
    assignments = [Assignment.from_canvas_api(a) for a in assignments_data]
    print(f"Found {len(assignments)} assignments")

    # Export to Excel
    print("\nExporting to Excel...")
    writer = ExcelWriter("my_assignments.xlsx")
    output_path = writer.write(assignments)

    print(f"✅ Export complete: {output_path}")

if __name__ == "__main__":
    main()
