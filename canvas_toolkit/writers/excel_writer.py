"""Excel export with formatting."""

import pandas as pd
from pathlib import Path
from typing import List
from ..models import Assignment


class ExcelWriter:
    """Export assignments to formatted Excel file."""

    def __init__(self, output_path: str = "canvas_assignments.xlsx"):
        """
        Initialize Excel writer.

        Args:
            output_path: Path for output Excel file
        """
        self.output_path = Path(output_path)

    def write(self, assignments: List[Assignment]) -> Path:
        """
        Write assignments to Excel with formatting.

        Args:
            assignments: List of Assignment objects

        Returns:
            Path to created Excel file
        """
        if not assignments:
            raise ValueError("No assignments to export")

        # Convert to DataFrame
        df = pd.DataFrame([a.to_dict() for a in assignments])

        # Add metadata columns (hidden from export)
        df['_is_overdue'] = [a.is_overdue for a in assignments]
        df['_html_url'] = [a.html_url for a in assignments]

        # Sort by due date (nulls last)
        df['_sort_key'] = pd.to_datetime(
            [a.due_at if a.due_at else '9999-12-31' for a in assignments],
            format='mixed',
            errors='coerce'
        )
        df = df.sort_values('_sort_key').drop('_sort_key', axis=1)

        # Create Excel writer with xlsxwriter engine for formatting
        with pd.ExcelWriter(self.output_path, engine='xlsxwriter') as writer:
            workbook = writer.book

            # Define formats
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

            link_format = workbook.add_format({
                'font_color': '#0563C1',
                'underline': True
            })

            # Write "All Assignments" sheet
            self._write_sheet(
                df, writer, "All Assignments",
                header_format, overdue_format, link_format
            )

            # Write per-course sheets
            for course_name in df['Course'].unique():
                course_df = df[df['Course'] == course_name]

                # Sanitize sheet name (Excel limits: 31 chars, no special chars)
                sheet_name = self._sanitize_sheet_name(course_name)

                self._write_sheet(
                    course_df, writer, sheet_name,
                    header_format, overdue_format, link_format
                )

        return self.output_path

    def _write_sheet(
        self,
        df: pd.DataFrame,
        writer: pd.ExcelWriter,
        sheet_name: str,
        header_format,
        overdue_format,
        link_format
    ):
        """Write a single sheet with formatting."""
        # Separate metadata columns from visible columns
        metadata_cols = ['_is_overdue', '_html_url']
        visible_cols = [col for col in df.columns if col not in metadata_cols]
        df_visible = df[visible_cols]

        # Write DataFrame (visible columns only)
        df_visible.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1, header=False)

        worksheet = writer.sheets[sheet_name]

        # Write headers with formatting
        for col_num, value in enumerate(df_visible.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Format columns
        worksheet.set_column('A:A', 30)  # Course
        worksheet.set_column('B:B', 40)  # Assignment
        worksheet.set_column('C:C', 18)  # Due Date
        worksheet.set_column('D:D', 10)  # Points
        worksheet.set_column('E:E', 20)  # Submission Type
        worksheet.set_column('F:F', 50)  # Canvas Link
        worksheet.set_column('G:G', 12)  # Canvas ID

        # Apply conditional formatting for overdue assignments
        # Iterate over sorted DataFrame rows (not original assignments list)
        for i in range(len(df)):
            row = df.iloc[i]
            row_num = i + 1  # Excel rows are 1-indexed, +1 for header

            # Apply overdue formatting
            if row['_is_overdue']:
                worksheet.set_row(row_num, None, overdue_format)

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
