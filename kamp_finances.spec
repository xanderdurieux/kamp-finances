# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('data', 'data'),  # Include the data directory
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'csv',
        'os',
        'datetime',
        'typing',
        'dataclasses',
        'src.main',
        'src.models.leader',
        'src.models.receipt',
        'src.models.expense',
        'src.services.data_service',
        'src.services.finance_service',
        'src.ui.main_window',
        'src.ui.tabs.leaders_tab',
        'src.ui.tabs.receipts_tab',
        'src.ui.tabs.pa_items_tab',
        'src.ui.tabs.poef_tab',
        'src.ui.components.base_components',
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
    name='KampFinances',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want a console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add path to icon file if you have one
) 