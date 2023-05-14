import sys
from cx_Freeze import setup, Executable

# List of files to be included in the package
files = [
    'run.py',
    'bot.py',
    'logo.ico', 
    'backtest.py',
    '__init__.py', 
    'setting.py',
    'utils.py',
    'bot_interface.py']

# Options for cx_Freeze
shortcut_table = [
    ("DesktopShortcut", 
    "DesktopFolder", "NSE BOT",
    "TARGETDIR", "[TARGETDIR]run.exe",
    None, None, None,"logo.ico",
    None, None, 'TARGETDIR',),
]

options = {
    'build_exe': {
        'include_files': files,
        'packages': ['os', 'sys', 'site', 'tkinter'],
    },
    "bdist_msi": {
        "upgrade_code": "{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}",
        "add_to_path": False,
        "initial_target_dir": "[ProgramFilesFolder]\\My App",
        "data": {
            "Shortcut": shortcut_table,
        },
    }
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

# Define the executable file
executables = [
    Executable('run.py', base=base, icon='logo.ico')
]

# Call the setup() function
setup(
    name='NSE BOT',
    version='1.0',
    description='this bot trades the stochastic cross',
    options=options,
    executables=executables
)
