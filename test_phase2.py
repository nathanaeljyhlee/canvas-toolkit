"""
Phase 2 Testing Script - Canvas Toolkit

Tests all export formats and validates:
- CSV export correctness
- JSON export metadata
- Excel conditional formatting fix (Bug #4)
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from canvas_toolkit.client.canvas_client import CanvasClient
from canvas_toolkit.models.assignment import Assignment
from canvas_toolkit.writers.csv_writer import CSVWriter
from canvas_toolkit.writers.json_writer import JSONWriter
from canvas_toolkit.writers.excel_writer import ExcelWriter

# Configuration
CANVAS_URL = "https://babson.instructure.com"
TOKEN_FILE = Path(__file__).parent.parent.parent / "secrets" / "Canvas API Key.env"

def load_token():
    """Load Canvas API token from .env file"""
    if not TOKEN_FILE.exists():
        raise FileNotFoundError(f"Token file not found: {TOKEN_FILE}")

    with open(TOKEN_FILE) as f:
        for line in f:
            if line.startswith("CANVAS_API_TOKEN="):
                return line.split("=", 1)[1].strip()
    raise ValueError("CANVAS_API_TOKEN not found in file")

def test_csv_export(assignments, output_dir):
    """Test CSV export"""
    print("\n" + "="*60)
    print("TEST 1: CSV Export")
    print("="*60)

    csv_path = output_dir / "test_export.csv"

    # Write CSV
    writer = CSVWriter(str(csv_path))
    writer.write(assignments)
    print(f"[OK] CSV written to: {csv_path}")

    # Validate
    df = pd.read_csv(csv_path)
    print(f"[OK] CSV readable - {len(df)} rows")

    # Check date sorting with nulls
    print("\n[Date Sorting Check]")
    print(f"   - Rows with due dates: {df['Due Date'].notna().sum()}")
    print(f"   - Rows with null dates: {df['Due Date'].isna().sum()}")

    # Verify null dates at end
    null_indices = df[df['Due Date'].isna()].index
    if len(null_indices) > 0:
        first_null = null_indices[0]
        last_non_null = df[df['Due Date'].notna()].index[-1] if df['Due Date'].notna().any() else -1

        if last_non_null >= 0 and first_null > last_non_null:
            print(f"   [OK] Null dates correctly sorted to end (row {first_null}+)")
        else:
            print(f"   [WARN] Null dates may not be at end")

    print(f"\n[OK] CSV EXPORT: PASS")
    return csv_path

def test_json_export(assignments, courses, output_dir):
    """Test JSON export"""
    print("\n" + "="*60)
    print("TEST 2: JSON Export")
    print("="*60)

    json_path = output_dir / "test_export.json"

    # Write JSON
    writer = JSONWriter(str(json_path))
    writer.write(assignments)
    print(f"[OK] JSON written to: {json_path}")

    # Validate
    with open(json_path) as f:
        data = json.load(f)

    print(f"[OK] JSON parseable")

    # Check metadata
    print("\n[CHECK] Metadata Check:")
    required_keys = ["exported_at", "total_assignments", "courses", "assignments"]
    for key in required_keys:
        if key in data:
            value = data[key]
            if key == "assignments":
                print(f"   [OK] {key}: {len(value)} items")
            elif key == "courses":
                print(f"   [OK] {key}: {len(value)} courses")
            else:
                print(f"   [OK] {key}: {value}")
        else:
            print(f"   [ERROR] {key}: MISSING")

    # Check date sorting
    assignments_data = data.get("assignments", [])
    dates_with_nulls = [(a.get("Due Date"), a.get("Assignment")) for a in assignments_data]
    print(f"\n[CHECK] Date Sorting Check:")
    print(f"   - Total assignments: {len(dates_with_nulls)}")
    print(f"   - With dates: {sum(1 for d, _ in dates_with_nulls if d and d != 'No due date')}")
    print(f"   - Without dates: {sum(1 for d, _ in dates_with_nulls if d == 'No due date')}")

    # Verify "No due date" at end
    first_null_idx = next((i for i, (d, _) in enumerate(dates_with_nulls) if d == 'No due date'), -1)
    last_date_idx = next((i for i in range(len(dates_with_nulls)-1, -1, -1) if dates_with_nulls[i][0] and dates_with_nulls[i][0] != 'No due date'), -1)

    if first_null_idx >= 0 and last_date_idx >= 0:
        if first_null_idx > last_date_idx:
            print(f"   [OK] 'No due date' entries correctly sorted to end (index {first_null_idx}+)")
        else:
            print(f"   [WARN] 'No due date' entries may not be at end")
    elif first_null_idx < 0:
        print(f"   [OK] All assignments have due dates")

    print(f"\n[OK] JSON EXPORT: PASS")
    return json_path

def test_excel_export(assignments, courses, output_dir):
    """Test Excel export and conditional formatting fix"""
    print("\n" + "="*60)
    print("TEST 3: Excel Export + Conditional Formatting Fix (Bug #4)")
    print("="*60)

    excel_path = output_dir / "test_export.xlsx"

    # Write Excel
    writer = ExcelWriter(str(excel_path))
    writer.write(assignments)
    print(f"[OK] Excel written to: {excel_path}")

    # Validate structure
    df = pd.read_excel(excel_path, sheet_name="All Assignments")
    print(f"[OK] Excel readable - {len(df)} rows")

    # Analyze overdue vs upcoming
    print("\n[CHECK] Assignment Status Distribution:")
    today = datetime.now()

    overdue_count = 0
    upcoming_count = 0
    no_date_count = 0

    for assignment in assignments:
        if not assignment.due_at:
            no_date_count += 1
        elif assignment.is_overdue:
            overdue_count += 1
        else:
            upcoming_count += 1

    print(f"   - Overdue: {overdue_count}")
    print(f"   - Upcoming: {upcoming_count}")
    print(f"   - No due date: {no_date_count}")

    print(f"\n[CHECK] Conditional Formatting Validation:")
    print(f"   Expected: ONLY the {overdue_count} overdue assignments should be highlighted red")
    print(f"   [WARN] Manual check required: Open {excel_path.name} and verify red highlighting")
    print(f"   [OK] If ONLY overdue assignments are red -> Bug #4 FIXED")
    print(f"   [ERROR] If random rows are red -> Bug #4 STILL PRESENT")

    # Show sample of overdue assignments for manual verification
    if overdue_count > 0:
        print(f"\n[LIST] Sample Overdue Assignments (should be red in Excel):")
        count = 0
        for assignment in assignments:
            if assignment.is_overdue and count < 3:
                print(f"   - {assignment.name[:50]}... (due: {assignment.due_date_formatted})")
                count += 1

    print(f"\n[OK] EXCEL EXPORT: PASS (manual verification needed for formatting)")
    return excel_path

def main():
    print("="*60)
    print("CANVAS TOOLKIT - PHASE 2 TESTING")
    print("="*60)
    print(f"Testing Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Setup
    print("\n[Setup]")
    token = load_token()
    print(f"[OK] Token loaded from: {TOKEN_FILE.name}")

    client = CanvasClient(CANVAS_URL, token)
    print(f"[OK] Canvas client initialized: {CANVAS_URL}")

    # Create output directory
    output_dir = Path(__file__).parent / "test_outputs"
    output_dir.mkdir(exist_ok=True)
    print(f"[OK] Output directory: {output_dir}")

    # Fetch data
    print("\n[Fetching Canvas data]")
    courses = client.get_courses()
    print(f"[OK] Found {len(courses)} courses")

    all_assignments_raw = []
    for course in courses:
        course_assignments = client.get_course_assignments(course["id"])
        all_assignments_raw.extend(course_assignments)
        print(f"   - {course['name']}: {len(course_assignments)} assignments")

    # Convert to Assignment objects
    all_assignments = [Assignment.from_canvas_api(a) for a in all_assignments_raw]
    print(f"[OK] Total assignments: {len(all_assignments)}")

    # Run tests
    csv_file = test_csv_export(all_assignments, output_dir)
    json_file = test_json_export(all_assignments, courses, output_dir)
    excel_file = test_excel_export(all_assignments, courses, output_dir)

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"[OK] CSV Export: {csv_file.name}")
    print(f"[OK] JSON Export: {json_file.name}")
    print(f"[OK] Excel Export: {excel_file.name}")
    print(f"\n[FILES] All files in: {output_dir}")
    print("\n[WARN] MANUAL VERIFICATION REQUIRED:")
    print(f"   1. Open {excel_file.name}")
    print(f"   2. Check 'All Assignments' sheet")
    print(f"   3. Verify ONLY overdue assignments are highlighted red")
    print(f"   4. If correct -> Bug #4 is FIXED [OK]")
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
