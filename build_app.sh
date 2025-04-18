#!/bin/bash

# Get ImageMagick path and binaries
MAGICK_PATH=$(which magick)
MAGICK_DIR=$(dirname "$MAGICK_PATH")

# Create a spec file for PyInstaller
cat > pq_converter.spec << EOL
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Collect binaries from ImageMagick directory
binaries = []
if "$MAGICK_PATH":
    import os
    magick_dir = "$MAGICK_DIR"
    for file in os.listdir(magick_dir):
        full_path = os.path.join(magick_dir, file)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            binaries.append((full_path, os.path.basename(full_path)))

a = Analysis(
    ['pq_converter.py'],
    pathex=[],
    binaries=binaries,
    datas=[('ITUR_2100_PQ_FULL.ICC', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PQ Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
EOL

# Build the application
pyinstaller pq_converter.spec

# Clean up
rm pq_converter.spec 