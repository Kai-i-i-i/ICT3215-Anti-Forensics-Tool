import subprocess
import sys

# Define the main script to compile
main_script = 'main.py'

# Define the command to run PyInstaller
command = [
    'pyinstaller',
    '--onefile',  # Create a single executable
    '--noconsole',  # Optional: Hide the console window (useful for GUI apps)
    main_script
]

# Run the command
try:
    subprocess.run(command, check=True)
    print(f'Successfully compiled {main_script} into an executable.')
except subprocess.CalledProcessError as e:
    print(f'Error during compilation: {e}', file=sys.stderr)