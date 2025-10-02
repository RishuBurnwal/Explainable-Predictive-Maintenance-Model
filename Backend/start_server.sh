#!/bin/bash
echo "Starting Explainable Predictive Maintenance Backend..."
echo

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Start the Flask application
echo "Starting Flask server on http://localhost:5000"
python app.py
