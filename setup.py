import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
includefiles = ['README.md', 'LICENSE', 'fonts//', 'images//', "gameProperties.txt"]
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], 'include_files':includefiles, "icon": "icon.ico"}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "monopoly",
        version = "1.0.0",
        description = "Monopoly : Python game Project",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Play.py", base=base)])
