# Quick Start Guide

Get up and running with the Explainable Predictive Maintenance Model in just a few simple steps.

## Prerequisites
- Node.js (v16 or later)
- Python (v3.8 or later)
- npm or yarn

## Quick Installation

### 1. Frontend Setup
```bash
cd FrontEnd
npm install
npm run dev
```

### 2. Backend Setup
```bash
cd Backend
pip install -r requirements.txt
python app.py
```

### 3. Access the Application
Open your browser and navigate to `http://localhost:5173` to access the application.

## IoT Sensor Integration

The system includes a complete IoT sensor network with 16 industrial sensors across 4 production lines:

1. **Turbofan Engines** (6 sensors)
2. **Hydraulic Systems** (3 sensors)
3. **Electric Motors** (3 sensors)
4. **Quality Control & Cooling** (4 sensors)

Sensors automatically initialize when the backend starts and update every 2 seconds.

## Accessing Sensor Features

1. Navigate to the Sensors page at `http://localhost:5173/sensors`
2. View all 16 sensors in real-time
3. Toggle sensors on/off using the switches
4. Monitor network health statistics
5. Filter sensors by status (All, Active, Critical, Warning)

## Testing the System

Run the provided test script to verify sensor functionality:
```bash
python test_sensors.py
```