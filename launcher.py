"""
Launcher script for Canvas Toolkit executable.

This script properly launches the Streamlit app when running as a PyInstaller bundle.
The normal `streamlit run` command doesn't work in frozen executables.
"""

import sys
import os
from pathlib import Path

# Add the bundle directory to Python path
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    bundle_dir = sys._MEIPASS
else:
    # Running as script
    bundle_dir = Path(__file__).parent

sys.path.insert(0, str(bundle_dir))

# Import Streamlit's main module
from streamlit.web import cli as stcli

def main():
    """Launch the Streamlit app."""
    # Path to the main app file
    app_path = Path(bundle_dir) / "canvas_toolkit.py"

    # Set up Streamlit arguments
    sys.argv = [
        "streamlit",
        "run",
        str(app_path),
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
        "--global.developmentMode=false",
    ]

    # Launch Streamlit
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()
