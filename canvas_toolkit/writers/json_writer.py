"""JSON export with metadata."""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from ..models import Assignment
from ..models.announcement import Announcement
from ..models.module import ModuleItem


class JSONWriter:
    """Export assignments to JSON file with metadata."""

    def __init__(self, output_path: str = "canvas_assignments.json"):
        """
        Initialize JSON writer.

        Args:
            output_path: Path for output JSON file
        """
        self.output_path = Path(output_path)

    def write(
        self,
        assignments: Optional[List[Assignment]] = None,
        announcements: Optional[List[Announcement]] = None,
        modules: Optional[List[ModuleItem]] = None,
        include_metadata: bool = True
    ) -> Path:
        """
        Write content to JSON.

        Args:
            assignments: List of Assignment objects
            announcements: List of Announcement objects
            modules: List of ModuleItem objects
            include_metadata: If True, include export metadata

        Returns:
            Path to created JSON file
        """
        if not any([assignments, announcements, modules]):
            raise ValueError("No content to export")

        # Build output structure
        output = {}

        if include_metadata:
            output["exported_at"] = datetime.now().isoformat()

        # Add assignments section
        if assignments:
            assignments_data = [assignment.to_dict() for assignment in assignments]
            # Sort by due date (assignments without due dates go to end)
            assignments_data.sort(
                key=lambda a: (a.get('Due Date') == 'No due date', a.get('Due Date', ''))
            )
            output["assignments"] = {
                "count": len(assignments),
                "data": assignments_data
            }

        # Add announcements section
        if announcements:
            announcements_data = [announcement.to_dict() for announcement in announcements]
            # Sort by posted date (newest first)
            announcements_data.sort(
                key=lambda a: a.get('Posted At', ''),
                reverse=True
            )
            output["announcements"] = {
                "count": len(announcements),
                "data": announcements_data
            }

        # Add modules section
        if modules:
            modules_data = [module.to_dict() for module in modules]
            # Maintain original order (module sequence is important)
            output["modules"] = {
                "count": len(modules),
                "data": modules_data
            }

        # Write JSON
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        return self.output_path
