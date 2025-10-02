@echo off
echo Starting Explainable Predictive Maintenance Backend...
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Start the Flask application
echo Starting Flask server on http://localhost:5000
python app.py

pause
