# Quick Start Guide

Get up and running with the Explainable Predictive Maintenance Model in just a few simple steps.

## Prerequisites
- Node.js (v16 or later)
- Python (v3.8 or later)
- Git (recommended)

## Quick Installation

### Option 1: Universal Setup Manager (Recommended)
```bash
# Run the universal setup manager
python setup_manager.py

# Follow the on-screen menu:
# 1. Check System Requirements
# 2. Complete Setup (Install Dependencies)
# 3. Run Both Frontend & Backend
```

### Option 2: Manual Setup

#### 1. Frontend Setup
```bash
cd FrontEnd
npm install
npm run dev
```

#### 2. Backend Setup
```bash
cd Backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 3. Access the Application
Open your browser and navigate to:
- **Main Dashboard**: `http://localhost:8080`
- **Sensors Page**: `http://localhost:8080/sensors`
- **Backend API**: `http://localhost:5000`

## IoT Sensor Integration

The system includes a complete IoT sensor network with 16 industrial sensors across 4 production lines:

1. **Turbofan Engines** (6 sensors)
   - Core Temperature Sensor
   - Fan Vibration Monitor
   - Compressor Pressure Gauge
   - Turbine RPM Sensor
   - Exhaust Temperature Probe
   - Bearing Vibration Sensor

2. **Hydraulic Systems** (3 sensors)
   - Hydraulic Pump Temperature
   - Hydraulic Pressure Sensor
   - Flow Rate Meter

3. **Electric Motors** (3 sensors)
   - Motor Current Sensor
   - Motor Voltage Monitor
   - Motor Torque Sensor

4. **Quality Control & Cooling** (4 sensors)
   - Spindle Temperature
   - Spindle Vibration
   - Coolant Temperature
   - Coolant Flow Meter

Sensors automatically initialize when the backend starts and update every 2 seconds.

## Accessing Sensor Features

1. Navigate to the Sensors page at `http://localhost:8080/sensors`
2. View all 16 sensors in real-time with status indicators
3. Toggle sensors on/off using the switches
4. Adjust sensor age/degradation settings (0-100%)
5. Monitor network health statistics in the dashboard
6. Filter sensors by status (All, Active, Inactive, Critical, Warning)
7. Filter sensors by location (Production Line A, B, C, etc.)

## Using the Main Dashboard

1. Access the main dashboard at `http://localhost:8080`
2. View real-time system status cards (Engine Status, RUL Prediction, Risk Level, Anomaly Status)
3. Monitor live data visualizations with real-time updates
4. Analyze AI explanations with SHAP/LIME feature importance
5. Receive smart alerts based on sensor health and predictions
6. Adjust update intervals (Real-time, 5s, 15s, etc.)

## Testing the System

### Backend API Testing
```bash
cd Backend
python test_api.py
```

### IoT Sensor Testing
```bash
python test_sensors.py
```

### Manual API Testing
You can also test the APIs manually:
- Health check: `GET http://localhost:5000/`
- All sensors: `GET http://localhost:5000/api/v1/sensors/sensors`
- Sensor statistics: `GET http://localhost:5000/api/v1/sensors/sensors/statistics`
- Predictions: `POST http://localhost:5000/api/v1/sensors/sensors/predict`

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   - Change frontend port in `FrontEnd/vite.config.ts`
   - Change backend port in `Backend/utils/config.py`

2. **Dependency Installation Failures**
   - Ensure Python virtual environment is activated
   - Check Node.js version (16+ required)
   - Clear npm cache: `npm cache clean --force`

3. **Connection Issues**
   - Verify both frontend and backend servers are running
   - Check CORS configuration in backend
   - Confirm API base URL in frontend (`FrontEnd/src/lib/api.ts`)

4. **Sensor Data Not Updating**
   - Check backend console for sensor manager errors
   - Verify sensor update interval in backend configuration
   - Ensure sensors are in "Active" state

### Verifying Installation

Successful installation should show:
- Frontend development server running on port 8080
- Backend Flask server running on port 5000
- Access to main dashboard at http://localhost:8080
- Access to sensors page at http://localhost:8080/sensors
- Healthy API responses from http://localhost:5000

## Next Steps

1. **Explore the Dashboard**: Familiarize yourself with the real-time monitoring features
2. **Experiment with Sensors**: Toggle sensors on/off and observe changes in predictions
3. **Adjust Settings**: Try different sensor age settings to see impact on RUL predictions
4. **Review Documentation**: Check `documentation/` folder for detailed guides
5. **Customize**: Add new sensors or modify existing ones in `Backend/AI/sensor_manager.py`