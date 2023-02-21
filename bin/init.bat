@ECHO off
@setlocal EnableDelayedExpansion

@ECHO KivyMD Project initialization
@SET /P "venv=Enter path to the venv folder: "
@SET /P "name=Enter venv name: "
@SET /P "pythonpath=Enter path to python distribution: "
@SET "folder_venv=%venv%\\%name%"
@SET "exe_path=%venv%\\%name%\\Scripts\\python.exe"
@SET "activate=%venv%\\%name%\\Scripts\\activate"
@SET "deactivate=%venv%\\%name%\\Scripts\\deactivate"

@ECHO Setting up project settings...
(@ECHO { && @ECHO "venv":"%folder_venv%" && @ECHO }) > ./config.json

@ECHO Creating virtual environment...
CALL %pythonpath% -m pip install virtualenv
CALL %pythonpath% -m virtualenv -p %pythonpath% %folder_venv%

@ECHO Installing packages...
CALL %activate%
@ECHO Working with virtual environment in %folder_venv%
CALL pip install -r requirements-win.txt
CALL %deactivate%
@ECHO Finished. Environment set as `%folder_venv%`.