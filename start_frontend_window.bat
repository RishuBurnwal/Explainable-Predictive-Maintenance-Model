@echo off
title Predictive Maintenance - Frontend Server
echo ===================================================
echo    Explainable Predictive Maintenance Frontend
echo    Developed by Rishu Burnwal
echo ===================================================
echo.
echo Starting frontend development server...
cd /d "%~dp0FrontEnd"

REM Install dependencies if node_modules doesn't exist
if not exist node_modules (
    echo Installing dependencies...
    npm install
)

REM Start the development server
echo Starting Vite development server on http://localhost:5173
npm run dev

echo.
echo Frontend server stopped.
pause
