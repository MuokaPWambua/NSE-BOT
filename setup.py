import sys
from cx_Freeze import setup, Executable

# List of files to be included in the package
files = ['/home/simba/Projects/Bot/run.py',
        '/home/simba/Projects/Bot/virtual',
        '/home/simba/Projects/Bot/bot.py', 
        '/home/simba/Projects/Bot/logo.png', 
        '/home/simba/Projects/Bot/backtest.py',
        '/home/simba/Projects/Bot/__init__.py', 
        '/home/simba/Projects/Bot/setting.py',
        '/home/simba/Projects/Bot/utils.py',
        '/home/simba/Projects/Bot/bot_interface.py']

# Options for cx_Freeze
options = {
    'build_exe': {
        'include_files': files,
        'packages': ['os', 'sys', 'site'],
    }
}

# Define the executable file
executables = [
    Executable('run.py', base=None)
]

# Call the setup() function
setup(
    name='NSE BOT',
    version='1.0',
    description='this bot trades the stochastic cross',
    options=options,
    executables=executables
)
