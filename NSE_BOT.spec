# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Add the virtual environment and other files to the Tree
venv_path = '/home/simba/Projects/Bot/virtual'
data_files = [('virtual', venv_path, 'virtual')]
other_files = ['bot.py', 'logo.png', 'run.py', 'backtest.py', '__init__.py', 'setting.py', 'utils.py', 'bot_interface.py']

a = Analysis(['run.py'],
             pathex=['/home/simba/Projects/Bot'],
             binaries=[],
             datas=other_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

tree = Tree(venv_path, prefix='virtual')

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='run',
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
        icon='logo.ico',)

# Include the Tree in the collection
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               [tree],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='dist/run')
