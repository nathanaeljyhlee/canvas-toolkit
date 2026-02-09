"""JSON export with metadata."""

import json
from pathlib import Path
from datetime import datetime
from typing import List
from ..models import Assignment


class JSONWriter:
    """Export assignments to JSON file with metadata."""

    def __init__(self, output_path: str = "canvas_assignments.json"):
        """
        Initialize JSON writer.

        Args:
            output_path: Path for output JSON file
        """
        self.output_path = Path(output_path)

    def write(self, assignments: List[Assignment], include_metadata: bool = True) -> Path:
        """
        Write assignments to JSON.

        Args:
            assignments: List of Assignment objects
            include_metadata: If True, include export metadata

        Returns:
            Path to created JSON file
        """
        if not assignments:
            raise ValueError("No assignments to export")

        # Convert to dict
        assignments_data = [assignment.to_dict() for assignment in assignments]

        # Sort by due date (assignments without due dates go to end)
        assignments_data.sort(
            key=lambda a: (a.get('Due Date') == 'No due date', a.get('Due Date', ''))
        )

        # Build output
        if include_metadata:
            output = {
                "exported_at": datetime.now().isoformat(),
                "total_assignments": len(assignments),
                "courses": list(set(a.course_name for a in assignments)),
                "assignments": assignments_data
            }
        else:
            output = assignments_data

        # Write JSON
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        return self.output_path
