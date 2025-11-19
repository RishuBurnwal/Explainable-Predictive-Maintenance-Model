# ⚡ Quick Start Guide - IoT Predictive Maintenance System

## 🚀 Start the System (3 Steps)

### Step 1: Start Backend
```bash
cd Backend
python app.py
```
✅ Wait for: `Running on http://127.0.0.1:5000`

### Step 2: Start Frontend
```bash
cd FrontEnd
npm run dev
```
✅ Wait for: `Local: http://localhost:8080`

### Step 3: Open Browser
- **Main Dashboard:** http://localhost:8080/
- **Sensors Page:** http://localhost:8080/sensors

---

## 📋 What You'll See

### Main Dashboard (/)
- **4 Status Cards:** Engine Status, RUL Prediction, Risk Level, Anomaly Status
- **Live Charts:** Real-time sensor data visualization
- **AI Explanations:** SHAP/LIME feature importance
- **Active Sensor Count:** Shows how many sensors are feeding data

### Sensors Page (/sensors)
- **16 Sensor Cards:** Each showing:
  - Name and location
  - Current reading with unit
  - Status (Normal/Warning/Critical)
  - Toggle switch to control
  - Real-time updates every 5 seconds

- **Statistics Dashboard:**
  - Total sensors: 16
  - Active/Inactive count
  - Critical/Warning alerts
  - Network health score

---

## 🎮 Try These Actions

1. **Go to Sensors Page** → Click "Sensors" in navigation
2. **Toggle a sensor OFF** → Use the switch on any sensor card
3. **Watch the change** → Status becomes "Offline"
4. **Toggle it back ON** → It resumes with new readings
5. **Filter sensors** → Click "Active Only" or "Critical"
6. **Go to Main Dashboard** → See sensor count update
7. **Watch live charts** → Click "Start Live Feed" button

---

## 🔧 Test the Backend

Run this test script:
```bash
python test_sensors.py
```

Expected output:
```
============================================================
IoT Sensor System Test
============================================================
Testing health endpoint...
Health check: healthy
Version: 2.1.0

Testing sensor endpoints...
Total sensors: 16
Sample sensor: Core Temperature Sensor

Testing AI predictions from sensors...
Predictions generated successfully!
RUL: XXX.XX hours
Active Sensors: 12

============================================================
All tests passed!
============================================================
```

---

## 🏭 Sensor Network

**16 Total Sensors across 4 production lines:**

### Production Line A (Turbofan Engines)
- Core Temperature, Fan Vibration, Compressor Pressure, Turbine RPM
- Exhaust Temperature, Bearing Vibration

### Production Line B (Hydraulic Systems)
- Pump Temperature, System Pressure, Flow Rate

### Production Line C (Electric Motors)
- Motor Current, Motor Voltage, Motor Torque

### Quality Control & Cooling
- Spindle Temperature, Spindle Vibration
- Coolant Temperature, Coolant Flow

---

## 📡 API Endpoints

**Test in browser or Postman:**

- Health: `http://localhost:5000/`
- All Sensors: `http://localhost:5000/api/v1/sensors/sensors`
- Statistics: `http://localhost:5000/api/v1/sensors/sensors/statistics`
- Real-time Data: `http://localhost:5000/api/v1/sensors/sensors/realtime-data`

---

## 🎯 Demo Checklist

For your presentation, demonstrate:

- [ ] Start backend and frontend
- [ ] Show main dashboard with live sensor count
- [ ] Navigate to Sensors page
- [ ] Explain a sensor card (name, location, description, reading)
- [ ] Toggle sensor OFF → Show status change
- [ ] Toggle sensor ON → Show it resume
- [ ] Show statistics update
- [ ] Use filters (Active, Critical)
- [ ] Return to dashboard and show charts updating
- [ ] Highlight "Live Sensor Data" indicator
- [ ] Explain AI predictions (RUL, Risk, Anomaly)

---

## ❓ Quick Troubleshooting

**Backend not starting?**
```bash
cd Backend
pip install -r requirements.txt
python app.py
```

**Frontend not starting?**
```bash
cd FrontEnd
npm install
npm run dev
```

**Sensors not visible?**
- Check backend is running: http://localhost:5000/
- Check browser console (F12) for errors
- Try refreshing the page (Ctrl+R)

**No real-time updates?**
- Verify both servers are running
- Check active sensor count
- Click "Refresh" button on sensors page

---

## 📊 Key Numbers

- **16 sensors** monitoring factory equipment
- **3 AI models** (XGBoost, LightGBM, Isolation Forest)
- **2-second** sensor update interval
- **5-second** auto-refresh on sensors page
- **15-second** dashboard updates
- **10+ API endpoints** for full control

---

## 🎓 For Presentation

**Opening Line:**
"This is a real-world IoT predictive maintenance system that monitors 16 industrial sensors across 4 production lines and uses AI to predict equipment failures before they happen."

**Key Points:**
1. Real sensor network simulation
2. Toggle sensors on/off in real-time
3. AI predictions adapt to active sensors
4. Industry-standard tech stack
5. Production-ready architecture

**Closing Line:**
"This system can reduce unplanned downtime by up to 50% and save millions in maintenance costs - it's ready for real-world deployment."

---

## 📁 Important Files

- `PROJECT_SUMMARY.md` - Complete documentation
- `IOT_SENSORS_GUIDE.md` - Detailed sensor guide
- `test_sensors.py` - Backend testing script
- `Backend/AI/sensor_manager.py` - Sensor system core
- `FrontEnd/src/pages/Sensors.tsx` - Sensors page
- `FrontEnd/src/lib/api.ts` - API client

---

## ✅ Success!

If you can:
1. ✅ Start both servers
2. ✅ See the main dashboard
3. ✅ Access the sensors page
4. ✅ Toggle sensors on/off
5. ✅ See real-time updates

**You're ready for your presentation! 🎉**

---

**Access Points:**
- 🌐 Main App: http://localhost:8080/
- 🔧 Sensors: http://localhost:8080/sensors
- 🔌 Backend API: http://localhost:5000/

**Good luck! 🚀**
