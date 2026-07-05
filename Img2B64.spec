# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['img2b64.py'],
    pathex=[],
    binaries=[('tk-bundle/usr/lib/libtk8.6.so', 'tcl-tk-lib'), ('tk-bundle/usr/lib/libtcl8.6.so', 'tcl-tk-lib')],
    datas=[('tk-bundle/usr/lib', 'tcl-tk-lib')],
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
    name='Img2B64',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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
    name='Img2B64',
)
