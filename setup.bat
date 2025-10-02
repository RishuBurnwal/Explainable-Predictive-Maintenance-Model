@echo off
echo Starting Explainable Predictive Maintenance Setup Manager...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Run the setup manager
python setup_manager.py

pause
