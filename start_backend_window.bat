@echo off
title Predictive Maintenance - Backend Server
echo ===================================================
echo    Explainable Predictive Maintenance Backend
echo    Developed by Rishu Burnwal
echo ===================================================
echo.
echo Starting backend server...
cd /d "%~dp0Backend"

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Start the Flask application
echo Starting Flask server on http://localhost:5000
python app.py

echo.
echo Backend server stopped.
pause
