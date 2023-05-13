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
options = {
    'build_exe': {
        'include_files': files,
        'packages': ['os', 'sys', 'site', 'tkinter'],
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
