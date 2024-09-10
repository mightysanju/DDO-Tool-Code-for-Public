import sys
from cx_Freeze import setup, Executable
import os

python_install_dir=os.path.dirname(sys.executable)
os.environ['TCL_LIBRARY']=os.path.join(python_install_dir,'tcl','tcl8.6')
os.environ['TK_LIBRARY']=os.path.join(python_install_dir,'tcl','tk8.6')

# include_files=[(os.path.join(python_install_dir,'DLLs','tk86t.dll'),os.path.join('lib','tk86.dll')),
#                (os.path.join(python_install_dir,'DLLs','tcl86t.dll'),os.path.join('lib','tcl86.dll'))]

# Dependencies are automatically detected, but it might need fine tuning.


folder_name='forest-dark'
build_exe_options = {   
                        "packages"              :["os","tkinter"],
                        "excludes"              :["unittest"],
                        "zip_include_packages"  :["encodings", "PySide6"],
                        "include_files"         :[(os.path.join(python_install_dir,'DLLs','tk86t.dll'),os.path.join('lib','tk86.dll')),
                                                 (os.path.join(python_install_dir,'DLLs','tcl86t.dll'),os.path.join('lib','tcl86.dll')),
                                                 'Network.ico','forest-dark.tcl',(folder_name,folder_name)],
                    }

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

executables=[Executable('DDO_Tool_v4Cx.py', base= base, 
                        icon= "Network.ico", 
                        shortcut_name='DDO Tool', shortcut_dir="DesktopFolder",)]

setup(
      name="DDO Tool",
      version="1.4.0",
      author='@sanjukuj',
      description="Defect Dispute Override Tool by @sanjukuj",
      options={"build_exe": build_exe_options },
      executables=executables
    )
