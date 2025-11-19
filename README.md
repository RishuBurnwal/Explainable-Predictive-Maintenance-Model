# 🛠️ Explainable Predictive Maintenance Model

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?logo=react)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.9.5-3178C6?logo=typescript)](https://www.typescriptlang.org/)

A cutting-edge software system for **Explainable Predictive Maintenance** with real-time visualization, designed for industrial equipment monitoring and failure prediction.

## ✨ Features

- **🎯 AI-Powered Predictions**: Advanced ML models for RUL (Remaining Useful Life) prediction
- **🔍 Explainable AI**: SHAP and LIME integration for model interpretability  
- **📊 Real-time Dashboard**: Interactive React TypeScript frontend with 3D animations
- **🔧 Robust Backend**: Flask-based REST API with comprehensive error handling
- **⚡ Live Monitoring**: Real-time anomaly detection and system health monitoring
- **📡 IoT Sensor Integration**: Real-time sensor data collection and processing
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

## 📂 Project Structure

```
Explainable Predictive Maintenance Model/
├── Backend/               # Flask backend
│   ├── AI/                # ML models and training
│   ├── api/               # API endpoints (prediction, anomaly, explainability, sensor)
│   ├── data/              # Sample datasets
│   └── models/            # Pretrained models
├── FrontEnd/              # React frontend
│   ├── src/               # Source code
│   │   ├── components/    # UI components
│   │   ├── pages/         # Page components (including Sensors page)
│   │   └── hooks/         # Custom hooks
│   └── public/            # Static files
├── documentation/         # Project documentation
└── setup_manager.py       # Universal setup script
```

## 🤖 ML Models

- **RUL Prediction**: XGBoost model for Remaining Useful Life estimation
- **Failure Prediction**: LightGBM classifier for failure probability
- **Anomaly Detection**: Isolation Forest for real-time anomaly identification

## 📊 Data Flow

1. **Data Ingestion**: Real-time sensor data collection
2. **Preprocessing**: Data cleaning and normalization
3. **Prediction**: ML model inference
4. **Explanation**: SHAP/LIME for model interpretability
5. **Visualization**: Interactive dashboard updates

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Rishu Burnwal**

- 📧 Email: [Gmail](mailto:rishuburnwal9525@gmail.com)
- 🔗 LinkedIn: [LinkedIn](https://linkedin.com/in/rishuburnwal)
- 🐙 GitHub: [GitHub](https://github.com/rishuburnwal)
- 🌐 Portfolio: [Portfolio](https://portfolio-ac8y.vercel.app/)

## 🙏 Acknowledgments

- NASA C-MAPSS dataset for providing the turbofan engine degradation simulation data
- Open-source community for the amazing libraries and tools used in this project