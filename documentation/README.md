# Explainable Predictive Maintenance Model

Welcome to the documentation for the Explainable Predictive Maintenance Model. This project leverages machine learning to predict equipment failures and provide explainable insights into the predictions.

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
│   ├── app.py
│   ├── requirements.txt
│   ├── AI/
│   │   ├── model_manager.py
│   │   ├── pretrained_models.py
│   │   └── sensor_manager.py
│   ├── api/
│   │   ├── prediction_api.py
│   │   ├── anomaly_api.py
│   │   ├── explainability_api.py
│   │   ├── data_api.py
│   │   └── sensor_api.py
│   ├── data/
│   ├── models/
│   └── utils/
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
│   └── LICENSE
├── setup_manager.py
├── test_sensors.py
└── IOT_SENSORS_GUIDE.md
```

## Getting Started

### Prerequisites
- Node.js (v16 or later)
- Python (v3.8 or later)
- npm or yarn
- Git

### Installation

1. **Frontend Setup**
   ```bash
   cd FrontEnd
   npm install
   npm run dev
   ```

2. **Backend Setup**
   ```bash
   cd Backend
   pip install -r requirements.txt
   python app.py
   ```

### Quick Start with Setup Manager
```bash
# Run the universal setup manager
python setup_manager.py

# Select option 3: "Run Both Frontend & Backend"
```

## Features

- Real-time equipment monitoring
- Predictive maintenance alerts
- Explainable AI insights
- Interactive data visualization
- Historical data analysis
- IoT sensor integration
- Real-time anomaly detection
- Sensor network management
- Live sensor data streaming
- Sensor health monitoring

## IoT Sensor Network

The system includes a complete industrial IoT sensor network with:

- **16 Industrial Sensors** across 4 production lines
- **Real-time Data Streaming** with 2-second update intervals
- **Sensor Control Interface** with toggle switches
- **Health Monitoring** with status indicators
- **Production Line A**: Turbofan Engines (6 sensors)
- **Production Line B**: Hydraulic Systems (3 sensors)
- **Production Line C**: Electric Motors (3 sensors)
- **Quality Control & Cooling**: (4 sensors)

## Technology Stack

### Frontend
- React 18 with TypeScript
- Vite for development
- TailwindCSS for styling
- Shadcn/ui components
- Recharts for visualizations
- React Router for navigation

### Backend
- Flask REST API
- Python 3.8+
- NumPy & Pandas
- Scikit-learn
- XGBoost & LightGBM
- SHAP & LIME
- Flask-CORS

### Machine Learning Models
- **RUL Prediction**: XGBoost model
- **Failure Prediction**: LightGBM classifier
- **Anomaly Detection**: Isolation Forest

## API Endpoints

### Prediction API
- `POST /api/v1/prediction/rul` - RUL prediction
- `POST /api/v1/prediction/failure-risk` - Failure risk classification
- `POST /api/v1/prediction/batch` - Batch predictions

### Explainability API
- `POST /api/v1/explainability/shap` - SHAP explanations
- `POST /api/v1/explainability/lime` - LIME explanations

### Anomaly API
- `POST /api/v1/anomaly/detect` - Anomaly detection

### Sensor API
- `GET /api/v1/sensors/sensors` - Get all sensors
- `GET /api/v1/sensors/sensors/{id}` - Get specific sensor
- `POST /api/v1/sensors/sensors/{id}/toggle` - Toggle sensor
- `GET /api/v1/sensors/sensors/statistics` - Network statistics
- `POST /api/v1/sensors/sensors/predict` - Predictions from sensors

### Data API
- `POST /api/v1/data/generate-sample` - Generate sample data

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.