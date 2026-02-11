"""Module and ModuleItem data models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List


@dataclass
class ModuleItem:
    """
    Standardized module item data model.

    Represents individual items within Canvas modules (assignments, pages,
    files, external URLs, etc.).
    """

    id: str
    module_id: str
    module_name: str
    course_id: str
    course_name: str
    position: int
    title: str
    type: str
    html_url: str
    published: bool
    indent: int = 0
    due_at: Optional[str] = None
    points_possible: Optional[float] = None

    @classmethod
    def from_canvas_api(cls, api_response: Dict[str, Any], module_name: str, course_id: str, course_name: str) -> "ModuleItem":
        """
        Create ModuleItem from Canvas API response.

        Args:
            api_response: Raw module item dict from Canvas API
            module_name: Name of parent module
            course_id: Canvas course ID
            course_name: Course name

        Returns:
            ModuleItem instance
        """
        # Extract content details if available
        content_details = api_response.get("content_details", {})
        due_at = content_details.get("due_at") if content_details else None
        points_possible = content_details.get("points_possible") if content_details else None

        return cls(
            id=str(api_response["id"]),
            module_id=str(api_response.get("module_id", "")),
            module_name=module_name,
            course_id=str(course_id),
            course_name=course_name,
            position=api_response.get("position", 0),
            title=api_response.get("title", "Untitled Item"),
            type=api_response.get("type", "Unknown"),
            html_url=api_response.get("html_url", ""),
            published=api_response.get("published", True),
            indent=api_response.get("indent", 0),
            due_at=due_at,
            points_possible=points_possible,
        )

    @property
    def title_with_indent(self) -> str:
        """Return title with indent spacing (2 spaces per indent level)."""
        indent_str = "  " * self.indent
        return f"{indent_str}{self.title}"

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

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for export."""
        return {
            "Course": self.course_name,
            "Module": self.module_name,
            "Item Title": self.title_with_indent,
            "Item Type": self.type,
            "Published": "Yes" if self.published else "No",
            "Due Date": self.due_date_formatted,
            "Points": self.points_possible if self.points_possible is not None else "N/A",
            "Canvas Link": self.html_url,
        }


@dataclass
class Module:
    """
    Container for module aggregation.

    Represents a Canvas module with its nested items.
    """

    id: str
    name: str
    course_id: str
    course_name: str
    items: List[ModuleItem] = field(default_factory=list)

    @classmethod
    def from_canvas_api(cls, api_response: Dict[str, Any], course_name: str) -> "Module":
        """
        Create Module from Canvas API response.

        Parses module and creates ModuleItem objects from nested items array.

        Args:
            api_response: Raw module dict from Canvas API
            course_name: Course name for item records

        Returns:
            Module instance with parsed items
        """
        module_id = str(api_response["id"])
        module_name = api_response.get("name", "Untitled Module")
        course_id = str(api_response.get("_course_id", ""))

        # Parse nested items if present
        items = []
        raw_items = api_response.get("items", [])
        for item_data in raw_items:
            try:
                item = ModuleItem.from_canvas_api(
                    api_response=item_data,
                    module_name=module_name,
                    course_id=course_id,
                    course_name=course_name
                )
                items.append(item)
            except (KeyError, ValueError) as e:
                # Skip malformed items
                continue

        return cls(
            id=module_id,
            name=module_name,
            course_id=course_id,
            course_name=course_name,
            items=items,
        )
