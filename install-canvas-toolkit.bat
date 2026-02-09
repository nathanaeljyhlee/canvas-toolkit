@echo off
echo ========================================
echo Canvas Toolkit Installer
echo ========================================
echo.
echo Installing Canvas Toolkit...
echo This will take 1-2 minutes.
echo.

pip install git+https://github.com/nathanaeljyhlee/canvas-toolkit.git

echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo Installation successful!
    echo ========================================
    echo.
    echo To launch Canvas Toolkit:
    echo 1. Double-click "run-canvas-toolkit.bat"
    echo 2. OR run: streamlit run canvas_toolkit.py
    echo.
    echo Your browser will open automatically.
    echo.
) else (
    echo ========================================
    echo Installation failed!
    echo ========================================
    echo.
    echo Please check:
    echo 1. Python is installed
    echo 2. You have internet connection
    echo 3. Run Command Prompt as Administrator
    echo.
)

pause
