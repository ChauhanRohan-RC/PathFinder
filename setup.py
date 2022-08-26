from cx_Freeze import setup, Executable
import os

main_dir = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options_pygame = {"packages": ["os", ], "excludes": ["tkinter", ]}
build_exe_options_tk = {"packages": ["os", ], "includes": ["tkinter", ]}

# GUI applications require a different TextBase on Windows (the default is for a
# console application).
base = "Win32GUI"

visualizer_pygame = Executable(script='Visualizer_Pygame.py',
                               icon=os.path.join(main_dir, 'icons\\path_finder.ico'),
                               base=base,
                               targetName='Path Finder (Pygame)')

visualizer_tk = Executable(script='Visualizer_Tk.py',
                               icon=os.path.join(main_dir, 'icons\\path_finder.ico'),
                               base=base,
                               targetName='Path Finder (TK)')

setup(name="RC PATH FINDER",
      version="1.0.0",
      description=f"Visualizer for Path Finding Algorithm",
      author="Rohan Chauhan",
      options={"build_exe": build_exe_options_tk},
      executables=[visualizer_pygame, visualizer_tk])