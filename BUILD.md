# Building Canvas Toolkit Executable

Guide for creating a standalone Windows executable (.exe) for Canvas Toolkit.

---

## Prerequisites

- Python 3.8+ installed
- All dependencies installed: `pip install -r requirements.txt`
- PyInstaller installed (included in requirements.txt)

---

## Quick Build (Windows)

**Option 1: Use the build script**

```bash
# Double-click build_exe.bat in Windows Explorer
# OR run from command prompt:
build_exe.bat
```

**Option 2: Manual build**

```bash
# Clean previous builds
rmdir /s /q build dist

# Run PyInstaller
pyinstaller canvas_toolkit.spec

# Executable will be in: dist/canvas_toolkit/canvas_toolkit.exe
```

---

## Build Time

- **First build:** 5-10 minutes (PyInstaller analyzes all dependencies)
- **Subsequent builds:** 2-5 minutes (cached dependencies)

---

## Build Output

### Directory Structure

```
dist/
└── canvas_toolkit/
    ├── canvas_toolkit.exe       # Main executable
    ├── _internal/               # Dependencies bundled here
    │   ├── streamlit/
    │   ├── pandas/
    │   ├── requests/
    │   └── ... (all dependencies)
    └── canvas_toolkit.py        # Main app file
```

### File Size

- **Total folder size:** ~150-200 MB
- **Executable size:** ~10 MB
- **Dependencies:** ~140-190 MB

**Why so large?** Streamlit and pandas include many dependencies (NumPy, Pillow, etc.)

---

## Testing the Executable

### Test on Development Machine

```bash
cd dist/canvas_toolkit
canvas_toolkit.exe
```

Your browser should open automatically to `http://localhost:8501`

### Test on Clean Machine (Important!)

To ensure the .exe works without Python installed:

1. Copy entire `dist/canvas_toolkit/` folder to USB drive
2. Transfer to a Windows machine **without Python**
3. Run `canvas_toolkit.exe`
4. Verify app launches and works correctly

**Common issues on clean machines:**
- Missing Visual C++ Runtime → Include redistributable
- Antivirus blocks executable → Sign the .exe or add exception
- Firewall blocks port 8501 → Allow through firewall

---

## Customization

### Change Executable Name

Edit `canvas_toolkit.spec`:

```python
exe = EXE(
    ...
    name='MyCustomName',  # Change this
    ...
)
```

### Add Application Icon

1. Create or download a `.ico` file (256x256 recommended)
2. Save as `icon.ico` in project root
3. Edit `canvas_toolkit.spec`:

```python
exe = EXE(
    ...
    icon='icon.ico',  # Add this
    ...
)
```

### Remove Console Window

Edit `canvas_toolkit.spec`:

```python
exe = EXE(
    ...
    console=False,  # Change True to False
    ...
)
```

**Warning:** Removing console hides error messages. Only do this after thorough testing.

---

## Troubleshooting

### Build Fails with "Module not found"

**Add to hidden imports in `canvas_toolkit.spec`:**

```python
hidden_imports = [
    'requests',
    'pandas',
    'YOUR_MISSING_MODULE',  # Add here
    ...
]
```

### Streamlit Not Found at Runtime

**Ensure Streamlit data files are collected:**

```python
streamlit_datas = collect_data_files('streamlit', include_py_files=True)
```

Already included in spec file.

### Executable Crashes Immediately

**Check console output:**

```bash
# Run from command prompt to see error messages
cd dist\canvas_toolkit
canvas_toolkit.exe
```

Common causes:
- Missing data files
- Incorrect path to `canvas_toolkit.py`
- Streamlit config issues

### App Works Locally but Not on Other Machines

**Likely causes:**
1. **Python installed on dev machine but not target** → .exe should be standalone
2. **Missing Visual C++ Runtime** → Include redistributable
3. **Different Windows version** → Test on target OS

---

## Distribution

### For Classmates

**Option 1: Zip the folder**

```bash
# Zip entire dist/canvas_toolkit/ folder
# Share via Google Drive, Dropbox, etc.
```

**Option 2: GitHub Release**

1. Create release tag (e.g., v1.0.0)
2. Upload `canvas_toolkit.zip` as release asset
3. Users download and extract

### For Public Release

**Consider:**
- Code signing certificate (avoids "Unknown publisher" warning)
- Installer (Inno Setup, NSIS) instead of zip
- Auto-updater (for future versions)

---

## Build Optimization

### Reduce Size (Optional)

**Exclude unused Streamlit features:**

Edit `canvas_toolkit.spec`:

```python
excludes=[
    'matplotlib',
    'plotly',
    'bokeh',
    'altair',  # Only if not used
]
```

**Use UPX compression (already enabled):**

```python
upx=True,  # Compresses binaries
```

---

## CI/CD (Future)

**Automate builds with GitHub Actions:**

```yaml
# .github/workflows/build.yml
name: Build Executable

on:
  release:
    types: [created]

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pyinstaller canvas_toolkit.spec
      - uses: actions/upload-artifact@v2
        with:
          name: canvas-toolkit-windows
          path: dist/canvas_toolkit/
```

---

## Support

**Build issues?**
- Check PyInstaller documentation: https://pyinstaller.org
- Check Streamlit + PyInstaller issues: https://github.com/streamlit/streamlit/issues
- Open issue on Canvas Toolkit repo

---

**Last updated:** Feb 9, 2026
