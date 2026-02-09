@echo off
REM Build script for Canvas Toolkit Windows executable

echo ========================================
echo Canvas Toolkit - Build Executable
echo ========================================
echo.

REM Clean previous build
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Cleaning previous builds...
echo.

REM Run PyInstaller
echo Building executable with PyInstaller...
echo This may take 5-10 minutes...
echo.

pyinstaller canvas_toolkit.spec

echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo Build successful!
    echo ========================================
    echo.
    echo Executable location: dist\canvas_toolkit\canvas_toolkit.exe
    echo.
    echo To test: cd dist\canvas_toolkit ^& canvas_toolkit.exe
    echo.
) else (
    echo ========================================
    echo Build failed!
    echo ========================================
    echo.
    echo Check the error messages above.
    echo.
)

pause
