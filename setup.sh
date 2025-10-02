#!/bin/bash
echo "Starting Explainable Predictive Maintenance Setup Manager..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Python is not installed or not in PATH!"
        echo "Please install Python 3.8+ from your package manager or https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Make the script executable
chmod +x setup_manager.py

# Run the setup manager
$PYTHON_CMD setup_manager.py
