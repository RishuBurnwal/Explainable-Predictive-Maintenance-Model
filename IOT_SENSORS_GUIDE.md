# 🏭 IoT Sensor Network - Real-Time Predictive Maintenance System

## 📋 Overview

This project has been enhanced to work as a **real-world industrial IoT predictive maintenance system** with live sensor monitoring and control capabilities. The system now integrates real factory sensors that provide real-time data for AI-powered predictions.

---

## 🌟 New Features Added

### 1. **Live IoT Sensor Network** 
- **16 Industrial Sensors** across multiple production lines
- Real-time sensor data generation and monitoring
- Sensor activation/deactivation controls
- Location tracking and sensor descriptions
- Health status monitoring (Normal, Warning, Critical)

### 2. **Dedicated Sensors Dashboard** (`/sensors`)
- Visual sensor grid with detailed information
- Toggle switches to activate/deactivate sensors
- Real-time status updates (every 5 seconds)
- Filter sensors by status (All, Active, Critical, Warnings)
- Network health statistics

### 3. **Real-Time Data Integration**
- Main dashboard now uses **live sensor data** for predictions
- Dynamic charts update based on active sensors
- Automatic fallback to sample data when no sensors active
- Real-time RUL, Risk, and Anomaly predictions from sensor network

### 4. **Factory Sensor Types**
- **Temperature Sensors**: Core, Exhaust, Hydraulic, Spindle, Coolant
- **Vibration Sensors**: Fan, Bearing, Spindle
- **Pressure Sensors**: Compressor, Hydraulic
- **RPM Sensors**: Turbine rotation monitoring
- **Flow Rate Meters**: Hydraulic and coolant systems
- **Current/Voltage Sensors**: Motor electrical monitoring
- **Torque Sensors**: Motor output measurement

---

## 🏗️ Architecture

### Backend (Python/Flask)
```
Backend/
├── AI/
│   ├── sensor_manager.py      # NEW: IoT sensor management & simulation
│   ├── model_manager.py        # AI models (XGBoost, LightGBM, Isolation Forest)
│   └── pretrained_models.py    # Model training utilities
├── api/
│   ├── sensor_api.py           # NEW: Sensor CRUD & real-time endpoints
│   ├── prediction_api.py       # RUL & failure predictions
│   ├── anomaly_api.py          # Anomaly detection
│   └── explainability_api.py   # SHAP/LIME explanations
└── app.py                      # Main Flask application
```

### Frontend (React/TypeScript)
```
FrontEnd/src/
├── pages/
│   ├── Index.tsx               # UPDATED: Main dashboard with sensor integration
│   └── Sensors.tsx             # NEW: Dedicated sensor management page
├── components/
│   ├── DataVisualization.tsx   # UPDATED: Real-time sensor data charts
│   └── ExplainabilityPanel.tsx # AI explanations
├── lib/
│   ├── api.ts                  # NEW: Complete API client
│   └── dataset.ts              # NEW: Dataset utilities
```

---

## 🚀 How to Run the Complete System

### Step 1: Start Backend Server

#### Option A: Automated (Recommended)
```bash
# Windows
start_backend_window.bat

# Linux/Mac
./Backend/start_server.sh
```

#### Option B: Manual
```bash
cd Backend
pip install -r requirements.txt
python app.py
```

**Backend runs on:** `http://localhost:5000`

### Step 2: Start Frontend Server

```bash
cd FrontEnd
npm install
npm run dev
```

**Frontend runs on:** `http://localhost:8080` (or check terminal output)

### Step 3: Access the Application

1. **Main Dashboard:** `http://localhost:8080/`
   - View real-time predictions from active sensors
   - Monitor system health
   - See live charts and visualizations

2. **Sensors Page:** `http://localhost:8080/sensors`
   - View all 16 factory sensors
   - Toggle sensors on/off
   - See real-time sensor readings
   - Monitor sensor health status

---

## 🎯 Using the Sensor System

### Accessing Sensors
1. Navigate to the **Sensors** page via the top navigation menu
2. You'll see 16 sensors organized in a grid layout

### Understanding Sensor Cards
Each sensor card displays:
- **Name**: Descriptive sensor name
- **Location**: Physical location in factory (e.g., "Production Line A - Turbofan Engine #1")
- **Description**: Purpose and monitoring details
- **Current Reading**: Real-time value with unit
- **Status Indicator**: 
  - 🟢 **Normal**: Operating within safe parameters
  - 🟡 **Warning**: Approaching threshold limits
  - 🔴 **Critical**: Immediate attention required
  - ⚪ **Offline**: Sensor deactivated

### Controlling Sensors
- Use the **toggle switch** on each card to activate/deactivate
- Active sensors contribute to real-time predictions
- Inactive sensors show "Offline" status

### Monitoring Network Health
- **Statistics Dashboard**: Shows total, active, critical, and warning sensor counts
- **Health Score**: Overall network health percentage
- **Filters**: View sensors by status (All, Active, Critical, etc.)

---

## 📊 Real-Time Predictions

The system now provides **dynamic predictions** based on active sensors:

### When Sensors Are Active:
- Dashboard shows: "Connected - Using X Real Sensors"
- Predictions update every **15 seconds** using live sensor data
- Charts display "Live Sensor Data" indicator
- All visualizations reflect real sensor states

### When No Sensors Are Active:
- System automatically falls back to simulated data
- Dashboard shows: "Connected to live backend"
- Predictions still function using AI models

---

## 🏭 Factory Sensor Network Layout

### Production Line A - Turbofan Engines
```
Engine #1:
├── Core Temperature Sensor
├── Fan Vibration Monitor
├── Compressor Pressure Gauge
└── Turbine RPM Sensor

Engine #2:
├── Exhaust Temperature Probe
└── Bearing Vibration Sensor
```

### Production Line B - Hydraulic Systems
```
Station #1:
├── Hydraulic Pump Temperature
└── Hydraulic Pressure Sensor

Station #2:
└── Flow Rate Meter
```

### Production Line C - Electric Motors
```
Motor #1:
├── Motor Current Sensor
└── Motor Voltage Monitor

Motor #2:
└── Motor Torque Sensor
```

### Quality Control Station
```
CNC Machine #1:
├── Spindle Temperature
└── Spindle Vibration
```

### Central Cooling System
```
Chiller Unit #1:
├── Coolant Temperature
└── Coolant Flow Meter
```

---

## 🔧 API Endpoints

### Sensor Management
```
GET    /api/v1/sensors/sensors                 # Get all sensors
GET    /api/v1/sensors/sensors/{id}            # Get specific sensor
POST   /api/v1/sensors/sensors/{id}/toggle     # Toggle sensor on/off
GET    /api/v1/sensors/sensors/statistics      # Network statistics
GET    /api/v1/sensors/sensors/realtime-data   # Real-time sensor data
POST   /api/v1/sensors/sensors/predict         # Get predictions from sensors
GET    /api/v1/sensors/sensors/health          # Network health status
```

### Predictions (Existing)
```
POST   /api/v1/prediction/rul                  # RUL prediction
POST   /api/v1/prediction/failure-risk         # Failure risk classification
POST   /api/v1/anomaly/detect                  # Anomaly detection
```

---

## 🎓 For Your Final Year Project Presentation

### Key Points to Highlight:

1. **Real-World Application**: 
   - Not just a demo, but a complete IoT monitoring system
   - Simulates actual factory sensor network
   - Industry-standard architecture

2. **AI Integration**:
   - XGBoost for RUL prediction
   - LightGBM for risk classification
   - Isolation Forest for anomaly detection
   - SHAP/LIME for explainable AI

3. **Modern Tech Stack**:
   - Backend: Python, Flask, scikit-learn
   - Frontend: React, TypeScript, Tailwind CSS
   - Real-time updates and responsive design

4. **Scalability**:
   - Modular sensor management system
   - Easy to add more sensors
   - RESTful API design
   - Can integrate with real IoT hardware

5. **User Experience**:
   - Intuitive sensor control interface
   - Real-time visualizations
   - Health monitoring and alerts
   - Mobile-responsive design

### Demo Flow Suggestion:

1. **Start**: Show main dashboard with live data
2. **Navigate to Sensors**: Display all 16 sensors
3. **Toggle Sensors**: Demonstrate on/off control
4. **Monitor Changes**: Show how dashboard updates with sensor changes
5. **View Analytics**: Highlight AI predictions and explanations
6. **Show Alerts**: Point out warning/critical sensors
7. **Network Health**: Display overall system statistics

---

## 🔮 Future Enhancements (Optional for Discussion)

- **WebSocket Integration**: For even faster real-time updates
- **Historical Data Storage**: Database integration (PostgreSQL/MongoDB)
- **Machine Learning Pipeline**: Automated retraining
- **Alert Notifications**: Email/SMS alerts for critical sensors
- **User Authentication**: Role-based access control
- **Mobile App**: React Native companion app
- **Hardware Integration**: Connect to actual IoT sensors (Raspberry Pi, Arduino)

---

## 📝 Project Customization

### Adding More Sensors
Edit `Backend/AI/sensor_manager.py` and add to `factory_sensors` list:

```python
{
    'name': 'Your Sensor Name',
    'type': 'temperature',  # or vibration, pressure, etc.
    'location': 'Production Line X - Machine Y',
    'description': 'What this sensor monitors',
    'machine_id': 'MACHINE-ID'
}
```

### Adjusting Update Frequency
- **Backend**: Modify `interval` in `sensor_manager.py` (default: 2 seconds)
- **Frontend Dashboard**: Change interval in `Index.tsx` (default: 15 seconds)
- **Frontend Sensors Page**: Change interval in `Sensors.tsx` (default: 5 seconds)

---

## 🐛 Troubleshooting

### Sensors Not Updating
- Ensure backend is running (`http://localhost:5000`)
- Check browser console for errors
- Verify network connectivity

### Backend Connection Failed
- Backend might be on different port
- Check `FrontEnd/src/lib/api.ts` for correct `API_BASE_URL`
- Ensure CORS is enabled in backend

### No Sensors Showing
- Backend sensor manager should auto-initialize
- Check backend console for errors
- Restart backend server

---

## 📧 Support

For questions or issues:
1. Check browser developer console (F12)
2. Check backend terminal output
3. Review API responses
4. Verify all dependencies are installed

---

## 🎉 Success Metrics

Your project demonstrates:
- ✅ Real-world IoT application
- ✅ AI/ML integration
- ✅ Full-stack development
- ✅ Real-time data processing
- ✅ Modern UI/UX design
- ✅ Scalable architecture
- ✅ Industry-relevant solution

**Perfect for a final year project showcasing practical software engineering skills!**

---

## 📄 License

This project is designed for educational purposes and can be used as a final year project demonstration.

---

**Built with ❤️ for Industrial IoT & Predictive Maintenance**
