# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['pq_converter.py'],
    pathex=[],
    binaries=[],
    datas=[('ITUR_2100_PQ_FULL.ICC', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pq_converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pq_converter',
)
app = BUNDLE(
    coll,
    name='pq_converter.app',
    icon=None,
    bundle_identifier=None,
)
