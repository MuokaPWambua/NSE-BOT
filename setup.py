import sys
from cx_Freeze import setup, Executable
from utils import resource_path

icon = resource_path('logo.ico')

# List of files to be included in the package
files = [
    'run.py',
    'bot.py',
    'logo.ico', 
    'backtest.py',
    '__init__.py', 
    'utils.py',
    'bot_interface.py']

# Options for cx_Freeze
shortcut_table = [
    ("DesktopShortcut", 
    "DesktopFolder", "NSE BOT",
    "TARGETDIR", "[TARGETDIR]run.exe",
    None, None, None, icon,
    None, None, 'TARGETDIR',),
]

options = {
    'build_exe': {
        'include_files': files,
        'packages': ['os', 'sys', 'site', 'tkinter', 'backtrader'],
    },
    "bdist_msi": {
        "upgrade_code": "{d42722e4-b464-46d8-bb7c-89f435c7c90d}",
        "add_to_path": False,
        "initial_target_dir": "[ProgramFilesFolder]\\NSE BOT",
        "data": {
            "Shortcut": shortcut_table,
        },
    }
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

# Define the executable file
executables = [
    Executable('run.py', base=base, icon=icon)
]

# Call the setup() function
setup(
    name='NSE BOT',
    version='1.0',
    description='NSE BOT',
    options=options,
    executables=executables
)
