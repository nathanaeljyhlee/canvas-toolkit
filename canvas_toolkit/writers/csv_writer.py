"""CSV export."""

import csv
from pathlib import Path
from typing import List
from ..models import Assignment


class CSVWriter:
    """Export assignments to CSV file."""

    def __init__(self, output_path: str = "canvas_assignments.csv"):
        """
        Initialize CSV writer.

        Args:
            output_path: Path for output CSV file
        """
        self.output_path = Path(output_path)

    def write(self, assignments: List[Assignment]) -> Path:
        """
        Write assignments to CSV.

        Args:
            assignments: List of Assignment objects

        Returns:
            Path to created CSV file
        """
        if not assignments:
            raise ValueError("No assignments to export")

        # Sort by due date (assignments without due dates go to end)
        sorted_assignments = sorted(
            assignments,
            key=lambda a: (a.due_at is None, a.due_at or '')
        )

        # Write CSV
        with open(self.output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'Course', 'Assignment', 'Due Date', 'Points',
                'Submission Type', 'Canvas Link', 'Canvas ID'
            ])

            writer.writeheader()
            for assignment in sorted_assignments:
                writer.writerow(assignment.to_dict())

        return self.output_path
