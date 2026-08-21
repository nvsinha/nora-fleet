@echo off
REM Nora Fleet Server Startup Script for Windows
REM This script handles all necessary steps to launch the nora-fleet server

setlocal enabledelayedexpansion

echo ===============================================
echo   Nora Fleet Server Startup
echo ===============================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..
cd /d "%PROJECT_DIR%"

echo Project directory: %PROJECT_DIR%
echo.

REM Check if virtual environment exists and recreate if needed
if exist ".venv" (
    echo Existing virtual environment found, removing to avoid outdated dependencies...
    rmdir /s /q .venv
)
if exist "venv" (
    rmdir /s /q venv
)

echo Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created
echo.

REM Activate virtual environment
set VENV_DIR=.venv

echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated
echo.

REM Set PYTHONPATH
set PYTHONPATH=%PROJECT_DIR%
echo PYTHONPATH set to: %PYTHONPATH%
echo.

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import nora_fleet" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed
) else (
    echo Dependencies already installed
)
echo.

REM Enable CORS headers for web applications
set AGENT_ALLOW_CORS_HEADERS=1
echo CORS headers enabled
echo.

REM Check if port is already in use
if not defined AGENT_HTTP_PORT set AGENT_HTTP_PORT=8080
netstat -ano | findstr ":%AGENT_HTTP_PORT%" | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 (
    echo ERROR: Port %AGENT_HTTP_PORT% is already in use!
    echo.
    echo To see what's using the port:
    echo   netstat -ano ^| findstr :%AGENT_HTTP_PORT%
    echo.
    echo To stop the process, find the PID and run:
    echo   taskkill /PID ^<PID^> /F
    echo.
    pause
    exit /b 1
)

REM Start the server
echo ===============================================
echo   Starting Nora Fleet Server on port %AGENT_HTTP_PORT%
echo ===============================================
echo.
echo Server will be available at: http://localhost:%AGENT_HTTP_PORT%
echo Press Ctrl+C to stop the server
echo.

python -m nora_fleet.service.main_loop.server_main_loop
