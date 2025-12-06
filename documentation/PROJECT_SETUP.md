# Project Setup

Detailed setup instructions and project structure for the Explainable Predictive Maintenance Model.

## Project Structure

```
Explainable Predictive Maintenance Model/
├── FrontEnd/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   ├── Navigation.tsx
│   │   │   ├── StatusCard.tsx
│   │   │   ├── DataVisualization.tsx
│   │   │   ├── ExplainabilityPanel.tsx
│   │   │   ├── DashboardSidebar.tsx
│   │   │   ├── AlertCard.tsx
│   │   │   └── Sensors.tsx
│   │   ├── pages/
│   │   │   ├── Index.tsx
│   │   │   ├── Documentation.tsx
│   │   │   ├── Sensors.tsx
│   │   │   └── NotFound.tsx
│   │   ├── lib/
│   │   │   └── api.ts
│   │   └── hooks/
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── README.md
├── Backend/
│   ├── AI/
│   │   ├── __init__.py
│   │   ├── model_manager.py
│   │   ├── pretrained_models.py
│   │   ├── sensor_manager.py
│   │   └── explainability.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── prediction_api.py
│   │   ├── explainability_api.py
│   │   ├── anomaly_api.py
│   │   ├── sensor_api.py
│   │   └── data_api.py
│   ├── app.py
│   ├── requirements.txt
│   ├── models/
│   ├── data/
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       └── logger.py
├── models/
│   ├── trained_models/
│   │   ├── xgboost_model.pkl
│   │   ├── scaler.pkl
│   │   └── feature_importance.json
│   ├── datasets/
│   │   ├── training_data.csv
│   │   ├── validation_data.csv
│   │   └── test_data.csv
│   └── notebooks/
│       ├── data_preprocessing.ipynb
│       ├── model_training.ipynb
│       └── evaluation.ipynb
├── documentation/
│   ├── README.md
│   ├── PROJECT_SETUP.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   ├── FAQ.md
│   ├── PROJECT_SUMMARY.md
│   ├── QUICK_START.md
│   └── LICENSE
├── setup_manager.py
├── test_sensors.py
├── IOT_SENSORS_GUIDE.md
├── QUICK_START.md
├── PROJECT_SUMMARY.md
├── setup.bat
├── setup.sh
├── start_backend_window.bat
├── start_frontend_window.bat
└── README.md
```

## Environment Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Frontend Dependencies
```bash
cd FrontEnd
npm install
```

### Backend Dependencies
```bash
cd Backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

### Backend Configuration
1. The backend automatically loads configuration from `Backend/utils/config.py`
2. Sensor update interval is set to 2 seconds by default
3. CORS is configured for localhost:8080 (Vite dev server)

### Frontend Configuration
1. The frontend configuration is in `FrontEnd/vite.config.ts`
2. API base URL is set to http://localhost:5000 by default
3. Port is set to 8080 by default

## IoT Sensor Setup

The system includes a simulation of 16 industrial sensors that automatically initialize when the backend starts. Sensors are organized across 4 production lines:

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

Sensors update every 2 seconds by default and can be controlled through the web interface at `/sensors`.

## Running the System

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

#### Start Backend
```bash
cd Backend
python app.py
```

#### Start Frontend
```bash
cd FrontEnd
npm run dev
```

### Access the Application
- **Main Dashboard**: http://localhost:8080/
- **Sensors Page**: http://localhost:8080/sensors
- **Backend API**: http://localhost:5000/
- **API Health Check**: http://localhost:5000/

## Testing

### Backend API Testing
```bash
cd Backend
python test_api.py
```

### IoT Sensor Testing
```bash
python test_sensors.py
```

## Development

### Backend Development
- Flask application entry point: `Backend/app.py`
- API endpoints: `Backend/api/`
- AI models: `Backend/AI/`
- Utilities: `Backend/utils/`

### Frontend Development
- React application entry point: `FrontEnd/src/main.tsx`
- Pages: `FrontEnd/src/pages/`
- Components: `FrontEnd/src/components/`
- API client: `FrontEnd/src/lib/api.ts`

### Adding New Sensors
To add new sensors, modify `Backend/AI/sensor_manager.py` and add entries to the `factory_sensors` list.

### Adding New ML Models
To add new ML models, modify `Backend/AI/model_manager.py` and add new model loading functions.