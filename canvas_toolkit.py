"""Canvas Assignment Exporter - Streamlit GUI"""

import streamlit as st
from pathlib import Path
from canvas_toolkit.client import CanvasClient, AuthenticationError, CanvasAPIError
from canvas_toolkit.models import Assignment
from canvas_toolkit.models.announcement import Announcement
from canvas_toolkit.models.module import Module, ModuleItem
from canvas_toolkit.writers import ExcelWriter, CSVWriter, JSONWriter


# Page config
st.set_page_config(
    page_title="Canvas Assignment Exporter",
    page_icon="📚",
    layout="centered"
)


def main():
    """Main Streamlit app."""

    st.title("📚 Canvas Assignment Exporter")
    st.markdown("Export your Canvas assignments to Excel, CSV, or JSON")
    st.divider()

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Canvas instance URL
        canvas_url = st.text_input(
            "Canvas URL",
            value="https://babson.instructure.com",
            help="Your Canvas instance URL (e.g., https://school.instructure.com)"
        )

        # API Token input with help
        with st.expander("ℹ️ How to get your Canvas API token"):
            st.markdown("""
            1. Log into Canvas
            2. Click **Account** → **Settings**
            3. Scroll to **Approved Integrations**
            4. Click **+ New Access Token**
            5. Enter purpose: "Canvas Toolkit Export"
            6. Click **Generate Token**
            7. Copy the token (shown only once!)
            """)

        api_token = st.text_input(
            "Canvas API Token",
            type="password",
            help="Your Canvas API access token"
        )

    # Main content
    if not api_token:
        st.info("👈 Enter your Canvas API token in the sidebar to get started")
        st.stop()

    # Initialize client
    try:
        client = CanvasClient(canvas_url, api_token)

        # Test connection (with caching to avoid repeated calls)
        if 'connection_tested' not in st.session_state:
            with st.spinner("Testing Canvas connection..."):
                client.test_connection()
                st.session_state.connection_tested = True
                st.success("✅ Connected to Canvas!")

    except AuthenticationError:
        st.error("❌ Invalid API token. Please check your token and try again.")
        st.stop()
    except CanvasAPIError as e:
        st.error(f"❌ Connection failed: {str(e)}")
        st.stop()

    # Fetch courses (with caching)
    @st.cache_data
    def fetch_courses(url, token):
        """Fetch courses with caching."""
        client = CanvasClient(url, token)
        return client.get_courses(include_concluded=False)

    with st.spinner("Fetching your courses..."):
        try:
            courses = fetch_courses(canvas_url, api_token)
        except CanvasAPIError as e:
            st.error(f"Failed to fetch courses: {str(e)}")
            st.stop()

    if not courses:
        st.warning("No active courses found")
        st.stop()

    # Course selection
    st.subheader("📖 Select Courses")

    # Option to select all
    select_all = st.checkbox("Select all courses", value=True)

    if select_all:
        selected_courses = {str(c['id']): c['name'] for c in courses}
    else:
        selected_courses = {}
        for course in courses:
            if st.checkbox(course['name'], key=f"course_{course['id']}"):
                selected_courses[str(course['id'])] = course['name']

    if not selected_courses:
        st.info("Select at least one course to export")
        st.stop()

    st.success(f"Selected {len(selected_courses)} course(s)")

    # Export options
    st.subheader("📥 Export Options")

    # Content type selection
    st.markdown("**Content to Export:**")
    col1, col2, col3 = st.columns(3)

    with col1:
        include_assignments = st.checkbox("📚 Assignments", value=True)
    with col2:
        include_announcements = st.checkbox("📢 Announcements", value=False, help="Last 30 days")
    with col3:
        include_modules = st.checkbox("📑 Modules", value=False)

    if not any([include_assignments, include_announcements, include_modules]):
        st.warning("⚠️ Select at least one content type")
        st.stop()

    st.divider()

    # Format and filename
    col1, col2 = st.columns(2)

    with col1:
        export_format = st.selectbox(
            "Export Format",
            options=["Excel", "CSV", "JSON"],
            help="Choose your preferred export format"
        )

    # Map format to file extension
    format_extensions = {
        "Excel": "xlsx",
        "CSV": "csv",
        "JSON": "json"
    }

    with col2:
        filename = st.text_input(
            "Filename",
            value=f"canvas_export.{format_extensions[export_format]}",
            help="Output filename"
        )

    # Filter options (only for assignments)
    if include_assignments:
        show_future_only = st.checkbox(
            "📅 Show only upcoming assignments",
            value=False,
            help="Filter out past assignments (due date >= today or no due date)"
        )
    else:
        show_future_only = False

    # Export button
    if st.button("📥 Export Content", type="primary", use_container_width=True):
        with st.spinner("Fetching content from Canvas..."):
            try:
                # Initialize content variables
                assignments = None
                announcements = None
                modules = None
                total_assignments = 0

                # Fetch assignments
                if include_assignments:
                    all_assignments_data = client.get_all_assignments(
                        course_ids=list(selected_courses.keys()),
                        include_concluded=False
                    )

                    # Convert to Assignment objects
                    all_assignments = [
                        Assignment.from_canvas_api(a)
                        for a in all_assignments_data
                    ]

                    total_assignments = len(all_assignments)

                    # Apply filter if requested
                    if show_future_only:
                        assignments = [
                            a for a in all_assignments
                            if a.is_upcoming or not a.due_at  # Include upcoming + no due date
                        ]
                    else:
                        assignments = all_assignments

                    if not assignments:
                        st.warning("No assignments found in selected courses" +
                                  (" (try unchecking 'Show only upcoming')" if show_future_only else ""))

                # Fetch announcements
                if include_announcements:
                    announcements_data = client.get_all_announcements(
                        course_ids=list(selected_courses.keys()),
                        days_back=30
                    )

                    # Convert to Announcement objects
                    announcements = [
                        Announcement.from_canvas_api(a)
                        for a in announcements_data
                    ]

                    # Sort by posted date (newest first) for consistent display
                    if announcements:
                        announcements.sort(key=lambda a: a.posted_at or "", reverse=True)

                    if not announcements:
                        st.info("No announcements found in the last 30 days")

                # Fetch modules
                if include_modules:
                    modules_data = client.get_all_modules(
                        course_ids=list(selected_courses.keys())
                    )

                    # Flatten modules to items
                    all_items = []
                    for mod_data in modules_data:
                        mod = Module.from_canvas_api(
                            mod_data,
                            mod_data["_course_name"]
                        )
                        all_items.extend(mod.items)

                    modules = all_items if all_items else None

                    if not modules:
                        st.info("No module items found")

                # Check if we have any content
                if not any([assignments, announcements, modules]):
                    st.error("No content found to export")
                    st.stop()

                # Export to selected format
                if export_format == "Excel":
                    writer = ExcelWriter(filename)
                    output_path = writer.write(
                        assignments=assignments,
                        announcements=announcements,
                        modules=modules
                    )
                elif export_format == "CSV":
                    # Generate separate CSV files for each content type
                    output_paths = []
                    if assignments:
                        csv_filename = filename.replace(".csv", "_assignments.csv")
                        writer = CSVWriter(csv_filename)
                        writer.write(assignments)
                        output_paths.append(csv_filename)
                    if announcements:
                        csv_filename = filename.replace(".csv", "_announcements.csv")
                        writer = CSVWriter(csv_filename)
                        writer.write(announcements)
                        output_paths.append(csv_filename)
                    if modules:
                        csv_filename = filename.replace(".csv", "_modules.csv")
                        writer = CSVWriter(csv_filename)
                        writer.write(modules)
                        output_paths.append(csv_filename)
                    output_path = output_paths[0]  # For download button
                else:  # JSON
                    writer = JSONWriter(filename)
                    output_path = writer.write(
                        assignments=assignments,
                        announcements=announcements,
                        modules=modules
                    )

                # Success message with stats
                st.success(f"✅ Export complete!")

                # Display stats
                col1, col2, col3 = st.columns(3)

                if assignments:
                    if show_future_only:
                        col1.metric("Assignments", len(assignments),
                                   delta=f"{total_assignments} total",
                                   delta_color="off")
                    else:
                        col1.metric("Assignments", len(assignments))
                else:
                    col1.metric("Assignments", 0)

                if announcements:
                    col2.metric("Announcements", len(announcements))
                else:
                    col2.metric("Announcements", 0)

                if modules:
                    col3.metric("Module Items", len(modules))
                else:
                    col3.metric("Module Items", 0)

                # Download button
                if export_format == "CSV" and len([x for x in [assignments, announcements, modules] if x]) > 1:
                    # Multiple CSV files created
                    st.info(f"📁 Created {len(output_paths)} CSV files: " + ", ".join([p for p in output_paths]))
                    st.markdown("*Files are saved in the current directory*")
                else:
                    # Single file download
                    with open(output_path, 'rb') as f:
                        st.download_button(
                            label=f"📄 Download {export_format} File",
                            data=f.read(),
                            file_name=filename if export_format != "CSV" else output_path,
                            mime={
                                'Excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                'CSV': 'text/csv',
                                'JSON': 'application/json'
                            }[export_format],
                            use_container_width=True
                        )

                # Preview
                with st.expander("📋 Preview"):
                    import pandas as pd

                    if assignments:
                        st.markdown("**Assignments (first 10):**")
                        preview_df = pd.DataFrame([a.to_dict() for a in assignments[:10]])
                        st.dataframe(preview_df, use_container_width=True)

                    if announcements:
                        st.markdown("**Announcements (first 10):**")
                        preview_df = pd.DataFrame([a.to_dict() for a in announcements[:10]])
                        st.dataframe(preview_df, use_container_width=True)

                    if modules:
                        st.markdown("**Module Items (first 10):**")
                        preview_df = pd.DataFrame([m.to_dict() for m in modules[:10]])
                        st.dataframe(preview_df, use_container_width=True)

            except CanvasAPIError as e:
                st.error(f"Export failed: {str(e)}")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
                st.exception(e)

    # Footer
    st.divider()
    st.markdown(
        "Built with ❤️ for MBA students | "
        "[Report an issue](https://github.com/nathanaeljyhlee/canvas-toolkit/issues)"
    )


if __name__ == "__main__":
    main()
