# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['pac-man.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('config/config.json', 'config'), ('venv/lib/python3.12/site-packages/mazegenerator', 'mazegenerator')],
    hiddenimports=['mazegenerator'],
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
    a.binaries,
    a.datas,
    [],
    name='pac-man',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='pac-man.app',
    icon=None,
    bundle_identifier=None,
)
