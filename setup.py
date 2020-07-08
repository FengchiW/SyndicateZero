from cx_Freeze import setup, Executable 
import os

include_files = ["res/"]

build_exe_options = {"includes": ["pygame"], "include_files": include_files}

icondir = os.getcwd()+'\icon.ico'

exe = Executable(
      script="client.py",
      base="Win32GUI",
      icon=icondir
     )
setup(
      name="Syndicate Zero",
      version="1.4.0",
      author="Wilson F. Wang",
      description="Testing Build",
      options = {"build_exe": build_exe_options},
      executables=[exe]
      )