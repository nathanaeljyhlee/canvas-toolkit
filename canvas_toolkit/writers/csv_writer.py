"""CSV export."""

import csv
from pathlib import Path
from typing import List
from ..models import Assignment
from ..models.announcement import Announcement
from ..models.module import ModuleItem


class CSVWriter:
    """Export assignments to CSV file."""

    def __init__(self, output_path: str = "canvas_assignments.csv"):
        """
        Initialize CSV writer.

        Args:
            output_path: Path for output CSV file
        """
        self.output_path = Path(output_path)

    def write(self, items: List) -> Path:
        """
        Write items to CSV.

        Args:
            items: List of Assignment, Announcement, or ModuleItem objects

        Returns:
            Path to created CSV file
        """
        if not items:
            raise ValueError("No items to export")

        # Convert all items to dictionaries using to_dict() method
        rows = [item.to_dict() for item in items]

        # Determine fieldnames from first item
        fieldnames = list(rows[0].keys())

        # Sort if applicable (assignments and announcements have dates)
        if isinstance(items[0], Assignment):
            # Sort by due date (assignments without due dates go to end)
            sorted_items = sorted(
                items,
                key=lambda a: (a.due_at is None, a.due_at or '')
            )
            rows = [item.to_dict() for item in sorted_items]
        elif isinstance(items[0], Announcement):
            # Sort by posted date (newest first)
            sorted_items = sorted(
                items,
                key=lambda a: a.posted_at or '',
                reverse=True
            )
            rows = [item.to_dict() for item in sorted_items]
        # ModuleItems don't need sorting (maintain module order)

        # Write CSV
        with open(self.output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for row in rows:
                writer.writerow(row)

        return self.output_path
