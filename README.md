# 🛠️ Explainable Predictive Maintenance Model

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?logo=react)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.9.5-3178C6?logo=typescript)](https://www.typescriptlang.org/)

A cutting-edge software system for **Explainable Predictive Maintenance** with real-time visualization, designed for industrial equipment monitoring and failure prediction.

**Now enhanced with a complete IoT sensor network featuring 16 industrial sensors across 4 production lines!**

## ✨ Features

- **🎯 AI-Powered Predictions**: Advanced ML models for RUL (Remaining Useful Life) prediction
- **🔍 Explainable AI**: SHAP and LIME integration for model interpretability  
- **📊 Real-time Dashboard**: Interactive React TypeScript frontend with 3D animations
- **🔧 Robust Backend**: Flask-based REST API with comprehensive error handling
- **⚡ Live Monitoring**: Real-time anomaly detection and system health monitoring
- **📡 IoT Sensor Integration**: Real-time sensor data collection and processing
- **🏭 Industrial IoT Network**: 16 sensors across 4 production lines (Turbofan Engines, Hydraulic Systems, Electric Motors, Quality Control)
- **🎛️ Sensor Control**: Toggle sensors on/off, adjust age/degradation settings
- **📈 Live Sensor Data**: Real-time sensor readings with status indicators (Normal, Warning, Critical)
- **🎨 Modern UI/UX**: Glass morphism design with smooth animations and responsive layout
- **🔄 Cross-Platform**: Universal setup manager for Windows, Linux, and macOS

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + TypeScript)                │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │   Dashboard     │ │  Visualizations │ │  Explainability │   │
│  │   Components    │ │    (Charts)     │ │   (SHAP/LIME)   │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │ REST API
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND (Flask + Python)                   │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │  Prediction API │ │ Explainability  │ │  Anomaly API    │   │
│  │   (RUL/Risk)    │ │   API (SHAP)    │ │  (Isolation)    │   │
│  │  Sensor API     │ │                 │ │                 │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                    IoT SENSOR NETWORK                           │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │ Turbofan Engine │ │ Hydraulic       │ │ Electric Motors │   │
│  │ Sensors (6)     │ │ Sensors (3)     │ │ Sensors (3)     │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
│  ┌─────────────────┐ ┌─────────────────┐                      │
│  │ Quality Control │ │ Cooling System  │                      │
│  │ Sensors (2)     │ │ Sensors (2)     │                      │
│  └─────────────────┘ └─────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/RishuBurnwal/Explainable-Predictive-Maintenance-Model.git
cd Explainable-Predictive-Maintenance-Model

# Run universal setup manager
python setup_manager.py

# Follow the on-screen instructions to start the application
```

### Alternative: Manual Setup

#### Backend Setup
```bash
cd Backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

#### Frontend Setup
```bash
cd FrontEnd
npm install
npm run dev
```

### Access the Application
- **Main Dashboard**: http://localhost:8080/
- **Sensors Page**: http://localhost:8080/sensors
- **Backend API**: http://localhost:5000/

## 📂 Project Structure

```
Explainable Predictive Maintenance Model/
├── Backend/               # Flask backend
│   ├── AI/                # ML models and training
│   │   ├── sensor_manager.py # IoT sensor network management
│   │   ├── model_manager.py  # AI model orchestration
│   │   └── pretrained_models.py # Pre-trained ML models
│   ├── api/               # API endpoints (prediction, anomaly, explainability, sensor)
│   │   ├── sensor_api.py   # IoT sensor endpoints
│   │   ├── prediction_api.py # RUL/failure prediction
│   │   ├── explainability_api.py # SHAP/LIME explanations
│   │   ├── anomaly_api.py  # Anomaly detection
│   │   └── data_api.py     # Data management
│   ├── data/              # Sample datasets
│   ├── models/            # Pretrained models
│   └── utils/             # Utility functions
├── FrontEnd/              # React frontend
│   ├── src/               # Source code
│   │   ├── components/    # UI components
│   │   │   ├── DataVisualization.tsx # Charts and graphs
│   │   │   ├── ExplainabilityPanel.tsx # SHAP/LIME visualizations
│   │   │   ├── StatusCard.tsx # Dashboard status cards
│   │   │   ├── AlertCard.tsx # Notification alerts
│   │   │   ├── Navigation.tsx # Site navigation
│   │   │   └── Sensors.tsx # IoT sensor dashboard
│   │   ├── pages/         # Page components (including Sensors page)
│   │   │   ├── Index.tsx   # Main dashboard
│   │   │   ├── Sensors.tsx # IoT sensor monitoring
│   │   │   └── Documentation.tsx # Documentation viewer
│   │   ├── lib/            # Utility libraries
│   │   │   └── api.ts      # API client
│   │   └── hooks/         # Custom hooks
│   └── public/            # Static files
├── documentation/         # Project documentation
├── setup_manager.py       # Universal setup script
├── test_sensors.py        # IoT sensor testing script
└── IOT_SENSORS_GUIDE.md   # Comprehensive sensor documentation
```

## 🤖 ML Models

- **RUL Prediction**: XGBoost model for Remaining Useful Life estimation
- **Failure Prediction**: LightGBM classifier for failure probability
- **Anomaly Detection**: Isolation Forest for real-time anomaly identification

## 🏭 IoT Sensor Network

The system now includes a complete industrial IoT sensor network with:

- **16 Industrial Sensors** across 4 production lines
- **Real-time Data Streaming** with 2-second update intervals
- **Sensor Control Interface** with toggle switches and age adjustment
- **Health Monitoring** with Normal, Warning, and Critical status indicators
- **Production Line A**: Turbofan Engines (6 sensors)
- **Production Line B**: Hydraulic Systems (3 sensors)
- **Production Line C**: Electric Motors (3 sensors)
- **Quality Control & Cooling**: (4 sensors)

## 📊 Data Flow

1. **IoT Sensor Network**: 16 industrial sensors continuously monitor equipment
2. **Data Ingestion**: Real-time sensor data collection every 2 seconds
3. **Preprocessing**: Data cleaning, normalization, and feature engineering
4. **Prediction**: ML model inference using sensor data
5. **Explanation**: SHAP/LIME for model interpretability
6. **Visualization**: Interactive dashboard updates with real-time charts
7. **Alerting**: Smart notifications based on sensor health and predictions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Rishu Burnwal**

- 📧 Email: [Gmail](mailto:rishuburnwal9525@gmail.com)
- 🔗 LinkedIn: [LinkedIn](https://linkedin.com/in/rishuburnwal)
- 🐙 GitHub: [GitHub](https://github.com/rishuburnwal)
- 🌐 Portfolio: [Portfolio](https://portfolio-ac8y.vercel.app/)

## 📞 Support

For questions, issues, or professional inquiries:
- Open an issue on GitHub
- Contact via email: rishuburnwal9525@gmail.com
- Connect on LinkedIn for collaboration opportunities

## 🙏 Acknowledgments

- NASA C-MAPSS dataset for providing the turbofan engine degradation simulation data
- Open-source community for the amazing libraries and tools used in this project
- Industrial IoT community for sensor network best practices