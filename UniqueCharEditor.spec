# -*- mode: python ; coding: utf-8 -*-
import sys
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# 收集 tkinter 需要的所有数据文件
datas = [
    ('unique_char_editor/assets/icon.ico', 'unique_char_editor/assets'),
]

# 添加 hiddenimports 以确保所有 tkinter 模块被包含
hiddenimports = ['tkinter', 'tkinter.ttk', 'tkinter.font', 'tkinter.filedialog', 'tkinter.messagebox']

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    exclude_binaries=True,  # onedir 模式：将二进制文件分离
    name='UniqueCharEditor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示终端窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='unique_char_editor/assets/icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='UniqueCharEditor',
)

app = BUNDLE(
    coll,
    name='UniqueCharEditor.app',
    icon='unique_char_editor/assets/icon.ico',
    bundle_identifier='com.xiaopu.uniquechareditor',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleName': 'UniqueCharEditor',
        'CFBundleDisplayName': 'UniqueCharEditor',
        'CFBundleGetInfoString': "獨特字元編輯器",
        'CFBundleIdentifier': 'com.xiaopu.uniquechareditor',
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "Copyright © 2025 XiaoPu. MIT License.",
        'NSHighResolutionCapable': True,
    },
)
