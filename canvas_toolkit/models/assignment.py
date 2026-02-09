"""Assignment data model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class Assignment:
    """Standardized assignment data model."""

    id: str
    name: str
    course_id: str
    course_name: str
    due_at: Optional[str]
    points_possible: Optional[float]
    html_url: str
    submission_types: list
    description: Optional[str] = None
    lock_at: Optional[str] = None
    unlock_at: Optional[str] = None
    has_submitted_submissions: bool = False

    @classmethod
    def from_canvas_api(cls, api_response: Dict[str, Any]) -> "Assignment":
        """
        Create Assignment from Canvas API response.

        Args:
            api_response: Raw assignment dict from Canvas API

        Returns:
            Assignment instance
        """
        return cls(
            id=str(api_response["id"]),
            name=api_response.get("name", "Untitled Assignment"),
            course_id=str(api_response.get("_course_id", "")),
            course_name=api_response.get("_course_name", "Unknown Course"),
            due_at=api_response.get("due_at"),
            points_possible=api_response.get("points_possible"),
            html_url=api_response.get("html_url", ""),
            submission_types=api_response.get("submission_types", []),
            description=api_response.get("description"),
            lock_at=api_response.get("lock_at"),
            unlock_at=api_response.get("unlock_at"),
            has_submitted_submissions=api_response.get("has_submitted_submissions", False),
        )

    @property
    def due_date_formatted(self) -> str:
        """Return formatted due date or 'No due date'."""
        if not self.due_at:
            return "No due date"
        try:
            dt = datetime.fromisoformat(self.due_at.replace('Z', '+00:00'))
            return dt.strftime("%m/%d/%Y %I:%M %p")
        except (ValueError, AttributeError):
            return self.due_at

    @property
    def submission_types_formatted(self) -> str:
        """Return comma-separated submission types."""
        if not self.submission_types:
            return "None"
        # Prettify submission type names
        formatted = []
        for sub_type in self.submission_types:
            formatted.append(sub_type.replace('_', ' ').title())
        return ", ".join(formatted)

    @property
    def is_overdue(self) -> bool:
        """Check if assignment is past due date."""
        if not self.due_at:
            return False
        try:
            due_date = datetime.fromisoformat(self.due_at.replace('Z', '+00:00'))
            return datetime.now(due_date.tzinfo) > due_date
        except (ValueError, AttributeError):
            return False

    @property
    def is_upcoming(self) -> bool:
        """Check if assignment is due in the future."""
        if not self.due_at:
            return False
        try:
            due_date = datetime.fromisoformat(self.due_at.replace('Z', '+00:00'))
            return datetime.now(due_date.tzinfo) < due_date
        except (ValueError, AttributeError):
            return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for export."""
        return {
            "Course": self.course_name,
            "Assignment": self.name,
            "Due Date": self.due_date_formatted,
            "Points": self.points_possible if self.points_possible else "N/A",
            "Submission Type": self.submission_types_formatted,
            "Canvas Link": self.html_url,
            "Canvas ID": self.id,
        }
