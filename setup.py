import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

build_exe_options = {'include_files':['get_price.py', 'chromedriver.exe', 'screen.py', 'form.ui', 'exact.png', 'ok.png', 'field_for_price.png', 'select.png']}
setup(  name = "poe_freeze",
        version = "0.2",
        description = "with cx_freeze, price setting",
        author_email='georgiyegor.burdin.l@gmail.com',
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base = "Win32GUI")]
        )

#python setup.py build