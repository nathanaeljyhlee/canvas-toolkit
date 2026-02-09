# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Canvas Toolkit Streamlit app.

Build command:
    pyinstaller canvas_toolkit.spec

This creates a standalone executable in dist/canvas_toolkit/
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all Streamlit data files and submodules
streamlit_datas = collect_data_files('streamlit', include_py_files=True)
streamlit_hiddenimports = collect_submodules('streamlit')

# Additional hidden imports for Canvas Toolkit
hidden_imports = [
    'requests',
    'pandas',
    'openpyxl',
    'xlsxwriter',
    'canvas_toolkit',
    'canvas_toolkit.client',
    'canvas_toolkit.models',
    'canvas_toolkit.writers',
    'canvas_toolkit.utils',
    'altair',  # Streamlit dependency
    'PIL',  # Streamlit dependency
    'watchdog',  # Streamlit file watcher
]

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=streamlit_datas + [('canvas_toolkit.py', '.')],  # Include main app as data file
    hiddenimports=streamlit_hiddenimports + hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',  # Exclude heavy unused deps
        'numpy',  # Already included via pandas
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='canvas_toolkit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Keep console for now (shows Streamlit logs)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # TODO: Add icon file if available
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='canvas_toolkit',
)
