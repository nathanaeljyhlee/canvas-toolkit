@echo off
echo Starting Canvas Toolkit...
echo Your browser will open automatically.
echo.
echo Keep this window open while using the app.
echo Press Ctrl+C to stop the app.
echo.

streamlit run "%~dp0canvas_toolkit.py"

pause
