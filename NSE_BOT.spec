# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['run.py'],
             pathex=['/home/simba/Projects/Bot'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

# Add the virtual environment and other files to the Tree
venv_path = '/home/simba/Projects/Bot/virtual'
data_files = [('virtual', venv_path, 'virtual')]
other_files = ['bot.py', 'logo.png', 'run.py', 'backtest.py', '__init__.py', 'setting.py', 'utils.py', 'bot_interface.py']
for file in other_files:
    data_files.append(('.', file, file))
tree = Tree('.', *data_files)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='NSE_BOT',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)

# Include the Tree in the collection
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               [tree],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='NSE_BOT')
