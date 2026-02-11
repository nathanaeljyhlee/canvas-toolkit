"""Test script for future-only assignments filter."""

from datetime import datetime, timedelta
from canvas_toolkit.models.assignment import Assignment


def create_test_assignment(name: str, due_at: str = None) -> Assignment:
    """Helper to create test assignment."""
    return Assignment(
        id=f"test_{name}",
        name=name,
        course_id="12345",
        course_name="Test Course",
        due_at=due_at,
        points_possible=100.0,
        html_url="https://test.com",
        submission_types=["online_text_entry"]
    )


def test_filter():
    """Test the filter logic."""

    # Create test assignments
    past = create_test_assignment(
        "Past Assignment",
        (datetime.now() - timedelta(days=7)).isoformat()
    )

    future = create_test_assignment(
        "Future Assignment",
        (datetime.now() + timedelta(days=7)).isoformat()
    )

    no_date = create_test_assignment("No Due Date Assignment", None)

    today = create_test_assignment(
        "Due Today",
        datetime.now().isoformat()
    )

    all_assignments = [past, future, no_date, today]

    # Apply filter (same logic as Streamlit app)
    filtered = [
        a for a in all_assignments
        if a.is_upcoming or not a.due_at
    ]

    # Results
    print("=" * 60)
    print("FILTER TEST RESULTS")
    print("=" * 60)
    print(f"\nTotal assignments: {len(all_assignments)}")
    print(f"Filtered (future + no date): {len(filtered)}")
    print(f"\nFiltered assignments:")

    for a in filtered:
        status = "No due date" if not a.due_at else "Future"
        print(f"  - {a.name} ({status})")

    print(f"\nExcluded assignments:")
    excluded = [a for a in all_assignments if a not in filtered]
    for a in excluded:
        status = "Overdue" if a.is_overdue else "Due today/now"
        print(f"  - {a.name} ({status})")

    # Verify logic
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)

    assert future in filtered, "Future assignment should be included"
    assert no_date in filtered, "No due date should be included"
    assert past not in filtered, "Past assignment should be excluded"

    # Edge case: "Due today" depends on exact time
    if today.is_upcoming:
        assert today in filtered, "If due later today, should be included"
        print("[PASS] 'Due today' is in the future (correct)")
    else:
        assert today not in filtered, "If due time passed, should be excluded"
        print("[PASS] 'Due today' time has passed (correct)")

    print("[PASS] Future assignments included")
    print("[PASS] No due date assignments included")
    print("[PASS] Past assignments excluded")
    print("\n[SUCCESS] All tests passed!")


if __name__ == "__main__":
    test_filter()
