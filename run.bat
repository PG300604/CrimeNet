@echo off
title CrimeNet Visualizer
echo =======================================================
echo          Starting CrimeNet Visualizer Server
echo =======================================================
echo.

cd /d "%~dp0"

:: Check for py launcher with Python 3.13
py -3.13 -c "import dash" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] Using Python 3.13 via py launcher...
    echo Starting server at http://127.0.0.1:8050/
    echo Press Ctrl+C in this window to stop the server.
    echo.
    py -3.13 visualizer\index.py
    goto :end
)

:: Check direct python path
if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    echo [OK] Using Python 3.13 from AppData...
    echo Starting server at http://127.0.0.1:8050/
    echo Press Ctrl+C in this window to stop the server.
    echo.
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" visualizer\index.py
    goto :end
)

:: Fallback to default python
python -c "import dash" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] Using default python command...
    echo Starting server at http://127.0.0.1:8050/
    echo Press Ctrl+C in this window to stop the server.
    echo.
    python visualizer\index.py
    goto :end
)

echo [ERROR] Could not find Python 3.13 with CrimeNet dependencies.
echo Please ensure Python 3.13 is installed or run with your virtual environment.
pause

:end
