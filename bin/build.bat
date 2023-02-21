@ECHO off
@setlocal EnableDelayedExpansion

@FOR /f "tokens=1,2 delims=:{} " %%A IN (config.json) DO (
    @set line=%%~B
    @set output=!line!
    @IF "!line:~-1!"=="," (
        @FOR /l %%i in (1,1,1000) do (
            @IF "!output:~-1!"=="," @set output=!output:~0,-1!
        )
        @FOR /l %%i in (1,1,1000) do (
            @IF "!output:~-1!"==" " @set output=!output:~0,-1!
        )
    )
    @SET %%~A=!output!
)
@SET "exe_path=%venv%\\Scripts\\python.exe"
@SET "activate=%venv%\\Scripts\\activate"
@SET "deactivate=%venv%\\Scripts\\deactivate"

@ECHO Working with virtual environment as %exe_path%
CALL %activate%
CALL pip install -r requirements-dev.txt
CALL python -m PyInstaller pieone.spec --noconfirm --log-level=WARN --workpath .\build\Windows --distpath .\dist\Windows
CALL %deactivate%
    