# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['tray_app/main.py'],
    pathex=['/home/server/code/nia_eng_page'],
    binaries=[],
    datas=[
        ('tray_app/config.json', 'tray_app'),
        ('pages', 'pages'),
        ('index.html', '.'),
    ],
    hiddenimports=[
        'pystray',
        'PIL',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
    ],
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
    name='nia-engineering-portal',
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
    icon=None,
)
