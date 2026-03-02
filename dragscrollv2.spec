# -*- mode: python ; coding: utf-8 -*-
# dragscrollv2.spec
#
# PyInstaller build spec for DragScrollV2.
#
# Key things this does:
#   - Bundles DragScroll.app INSIDE DragScrollV2.app (so users don't need to
#     install it separately - dragscrollv2.py copies it to /Applications on
#     first launch)
#   - Sets LSUIElement=True so the app is menu bar only (no Dock icon)
#   - Uses the custom mouse icon

block_cipher = None

a = Analysis(
    ['src/dragscrollv2.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('icon.png', '.'),
        # Bundle DragScroll.app inside our app - dragscrollv2.py extracts it
        # to /Applications on first launch so 'open -a DragScroll' works
        ('/Applications/DragScroll.app', 'DragScroll.app'),
    ],
    hiddenimports=[
        'rumps',
        'subprocess',
        'json',
        'pathlib',
        'Foundation',
        'AppKit',
        'objc',
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
    [],
    exclude_binaries=True,
    name='DragScrollV2',
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
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DragScrollV2',
)

app = BUNDLE(
    coll,
    name='DragScrollV2.app',
    icon='icon.png',
    bundle_identifier='com.gitwrecked5on.dragscrollv2',
    info_plist={
        'CFBundleName': 'DragScrollV2',
        'CFBundleDisplayName': 'DragScrollV2',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'MIT License - gitwrecked5on',
        # CRITICAL: menu bar only - suppresses the Dock icon
        'LSUIElement': True,
        'NSAppleEventsUsageDescription': 'DragScrollV2 needs accessibility access to control drag scrolling.',
    },
)
