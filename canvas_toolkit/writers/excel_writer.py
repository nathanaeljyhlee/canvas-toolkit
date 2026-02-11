"""Excel export with formatting."""

import pandas as pd
from pathlib import Path
from typing import List, Optional
import xlsxwriter
from ..models import Assignment
from ..models.announcement import Announcement
from ..models.module import ModuleItem


class ExcelWriter:
    """Export assignments to formatted Excel file."""

    def __init__(self, output_path: str = "canvas_assignments.xlsx"):
        """
        Initialize Excel writer.

        Args:
            output_path: Path for output Excel file
        """
        self.output_path = Path(output_path)

    def write(
        self,
        assignments: Optional[List[Assignment]] = None,
        announcements: Optional[List[Announcement]] = None,
        modules: Optional[List[ModuleItem]] = None
    ) -> Path:
        """
        Write assignments, announcements, and/or modules to Excel with formatting.

        Args:
            assignments: Optional list of Assignment objects
            announcements: Optional list of Announcement objects
            modules: Optional list of ModuleItem objects

        Returns:
            Path to created Excel file
        """
        if not any([assignments, announcements, modules]):
            raise ValueError("No content to export")

        workbook = xlsxwriter.Workbook(str(self.output_path))

        # Define formats (reused across all sheets)
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4472C4',
            'font_color': 'white',
            'border': 1
        })

        overdue_format = workbook.add_format({
            'bg_color': '#FFC7CE',
            'font_color': '#9C0006'
        })

        upcoming_format = workbook.add_format({
            'bg_color': '#FFEB9C',
            'font_color': '#9C6500'
        })

        recent_format = workbook.add_format({
            'bg_color': '#E8F5E9',
            'border': 1
        })

        link_format = workbook.add_format({
            'font_color': '#0563C1',
            'underline': True
        })

        # Write assignments sheet if provided
        if assignments:
            worksheet = workbook.add_worksheet("All Assignments")
            self._write_assignments_sheet(workbook, worksheet, assignments, header_format, overdue_format, upcoming_format, link_format)

        # Write announcements sheet if provided
        if announcements:
            worksheet = workbook.add_worksheet("All Announcements")
            self._write_announcements_sheet(workbook, worksheet, announcements, header_format, recent_format, link_format)

        # Write modules sheet if provided
        if modules:
            worksheet = workbook.add_worksheet("All Modules")
            self._write_modules_sheet(workbook, worksheet, modules, header_format, link_format)

        workbook.close()
        return self.output_path

    def _write_assignments_sheet(
        self,
        workbook,
        worksheet,
        assignments: List[Assignment],
        header_format,
        overdue_format,
        upcoming_format,
        link_format
    ):
        """Write assignments sheet with formatting."""
        # Convert to DataFrame
        df = pd.DataFrame([a.to_dict() for a in assignments])

        # Add metadata columns (hidden from export)
        df['_is_overdue'] = [a.is_overdue for a in assignments]
        df['_is_upcoming'] = [a.is_upcoming for a in assignments]
        df['_html_url'] = [a.html_url for a in assignments]

        # Sort by due date (nulls last)
        df['_sort_key'] = pd.to_datetime(
            [a.due_at if a.due_at else '9999-12-31' for a in assignments],
            format='mixed',
            errors='coerce'
        )
        df = df.sort_values('_sort_key').drop('_sort_key', axis=1)

        # Separate metadata columns from visible columns
        metadata_cols = ['_is_overdue', '_is_upcoming', '_html_url']
        visible_cols = [col for col in df.columns if col not in metadata_cols]
        df_visible = df[visible_cols]

        # Write headers with formatting
        for col_num, value in enumerate(df_visible.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Write data rows
        for row_num, (_, row) in enumerate(df_visible.iterrows(), start=1):
            for col_num, value in enumerate(row):
                worksheet.write(row_num, col_num, value)

        # Format columns
        worksheet.set_column('A:A', 30)  # Course
        worksheet.set_column('B:B', 40)  # Assignment
        worksheet.set_column('C:C', 18)  # Due Date
        worksheet.set_column('D:D', 10)  # Points
        worksheet.set_column('E:E', 20)  # Submission Type
        worksheet.set_column('F:F', 50)  # Canvas Link
        worksheet.set_column('G:G', 12)  # Canvas ID

        # Apply conditional formatting
        for i in range(len(df)):
            row = df.iloc[i]
            row_num = i + 1  # Excel rows are 1-indexed, +1 for header

            # Apply overdue formatting (priority over upcoming)
            if row['_is_overdue']:
                worksheet.set_row(row_num, None, overdue_format)
            elif row['_is_upcoming']:
                worksheet.set_row(row_num, None, upcoming_format)

            # Make Canvas Link clickable
            if row['_html_url']:
                worksheet.write_url(
                    row_num, 5,  # Column F (0-indexed)
                    row['_html_url'],
                    link_format,
                    string="Open in Canvas"
                )

        # Freeze header row
        worksheet.freeze_panes(1, 0)

        # Add autofilter
        worksheet.autofilter(0, 0, len(df), len(df_visible.columns) - 1)

    def _write_announcements_sheet(
        self,
        workbook,
        worksheet,
        announcements: List[Announcement],
        header_format,
        recent_format,
        link_format
    ):
        """Write announcements sheet with formatting."""
        # Convert to DataFrame
        data = []
        for ann in announcements:
            ann_dict = ann.to_dict()
            ann_dict['_is_recent'] = ann.is_recent
            ann_dict['_html_url'] = ann.html_url
            data.append(ann_dict)

        df = pd.DataFrame(data)

        # Sort by posted date descending (newest first)
        df['_sort_key'] = pd.to_datetime(df['Posted Date'], format='mixed', errors='coerce')
        df = df.sort_values('_sort_key', ascending=False).drop('_sort_key', axis=1)

        # Separate metadata columns from visible columns
        metadata_cols = ['_is_recent', '_html_url']
        visible_cols = [col for col in df.columns if col not in metadata_cols]
        df_visible = df[visible_cols]

        # Write headers with formatting
        headers = ['Course', 'Title', 'Posted Date', 'Author', 'Message Preview', 'Embedded Links', 'Attachments', 'Canvas Link']
        for col_num, value in enumerate(headers):
            worksheet.write(0, col_num, value, header_format)

        # Write data rows
        for row_num, (_, row) in enumerate(df_visible.iterrows(), start=1):
            for col_num, value in enumerate(row):
                worksheet.write(row_num, col_num, value)

        # Format columns
        worksheet.set_column('A:A', 20)  # Course
        worksheet.set_column('B:B', 30)  # Title
        worksheet.set_column('C:C', 18)  # Posted Date
        worksheet.set_column('D:D', 15)  # Author
        worksheet.set_column('E:E', 50)  # Message Preview
        worksheet.set_column('F:F', 12)  # Embedded Links
        worksheet.set_column('G:G', 12)  # Attachments
        worksheet.set_column('H:H', 15)  # Canvas Link

        # Apply conditional formatting
        for i in range(len(df)):
            row = df.iloc[i]
            row_num = i + 1  # Excel rows are 1-indexed, +1 for header

            # Apply recent formatting
            if row['_is_recent']:
                worksheet.set_row(row_num, None, recent_format)

            # Make Canvas Link clickable
            if row['_html_url']:
                worksheet.write_url(
                    row_num, 7,  # Column H (0-indexed)
                    row['_html_url'],
                    link_format,
                    string="Open in Canvas"
                )

        # Freeze header row
        worksheet.freeze_panes(1, 0)

        # Add autofilter
        worksheet.autofilter(0, 0, len(df), len(headers) - 1)

    def _write_modules_sheet(
        self,
        workbook,
        worksheet,
        modules: List[ModuleItem],
        header_format,
        link_format
    ):
        """Write modules sheet with formatting."""
        # Convert to DataFrame
        data = []
        for mod in modules:
            mod_dict = mod.to_dict()
            mod_dict['_html_url'] = mod.html_url
            data.append(mod_dict)

        df = pd.DataFrame(data)

        # NO sorting - preserve natural API order (module structure)

        # Separate metadata columns from visible columns
        metadata_cols = ['_html_url']
        visible_cols = [col for col in df.columns if col not in metadata_cols]
        df_visible = df[visible_cols]

        # Write headers with formatting
        headers = ['Course', 'Module', 'Item Title', 'Item Type', 'Published', 'Due Date', 'Points', 'Canvas Link']
        for col_num, value in enumerate(headers):
            worksheet.write(0, col_num, value, header_format)

        # Write data rows
        for row_num, (_, row) in enumerate(df_visible.iterrows(), start=1):
            for col_num, value in enumerate(row):
                worksheet.write(row_num, col_num, value)

        # Format columns
        worksheet.set_column('A:A', 20)  # Course
        worksheet.set_column('B:B', 25)  # Module
        worksheet.set_column('C:C', 40)  # Item Title
        worksheet.set_column('D:D', 15)  # Item Type
        worksheet.set_column('E:E', 10)  # Published
        worksheet.set_column('F:F', 18)  # Due Date
        worksheet.set_column('G:G', 8)   # Points
        worksheet.set_column('H:H', 15)  # Canvas Link

        # Apply conditional formatting
        for i in range(len(df)):
            row = df.iloc[i]
            row_num = i + 1  # Excel rows are 1-indexed, +1 for header

            # Make Canvas Link clickable
            if row['_html_url']:
                worksheet.write_url(
                    row_num, 7,  # Column H (0-indexed)
                    row['_html_url'],
                    link_format,
                    string="Open in Canvas"
                )

        # Freeze header row
        worksheet.freeze_panes(1, 0)

        # Add autofilter
        worksheet.autofilter(0, 0, len(df), len(headers) - 1)

    @staticmethod
    def _sanitize_sheet_name(name: str) -> str:
        """
        Sanitize sheet name for Excel compatibility.

        Excel sheet names must be:
        - <= 31 characters
        - Cannot contain: \\ / ? * [ ] :
        """
        # Remove invalid characters
        for char in ['\\', '/', '?', '*', '[', ']', ':']:
            name = name.replace(char, ' ')

        # Remove multiple spaces and trim
        name = ' '.join(name.split())

        # Truncate to 31 characters
        if len(name) > 31:
            name = name[:28] + "..."

        return name
