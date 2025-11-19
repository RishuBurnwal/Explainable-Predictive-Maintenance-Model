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
│   │   │   └── DashboardSidebar.tsx
│   │   ├── pages/
│   │   │   ├── Index.tsx
│   │   │   ├── Documentation.tsx
│   │   │   ├── Sensors.tsx
│   │   │   └── ...
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── assets/
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── README.md
├── Backend/
│   ├── AI/
│   │   ├── __init__.py
│   │   ├── model_manager.py
│   │   ├── pretrained_models.py
│   │   └── sensor_manager.py
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
│   ├── routes/
│   └── utils/
└── models/
    ├── trained_models/
    │   ├── xgboost_model.pkl
    │   ├── scaler.pkl
    │   └── feature_importance.json
    ├── datasets/
    │   ├── training_data.csv
    │   ├── validation_data.csv
    │   └── test_data.csv
    └── notebooks/
        ├── data_preprocessing.ipynb
        ├── model_training.ipynb
        └── evaluation.ipynb
```

## Environment Setup

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

1. Create a `.env` file in the Backend directory with the following variables:
```
PORT=5000
NODE_ENV=development
DATABASE_URL=your_database_connection_string
SENSOR_UPDATE_INTERVAL=2
```

2. Update the frontend configuration in `FrontEnd/vite.config.ts` if needed.

## IoT Sensor Setup

The system includes a simulation of 16 industrial sensors that automatically initialize when the backend starts. Sensors are organized across 4 production lines:

1. **Turbofan Engines** (6 sensors)
2. **Hydraulic Systems** (3 sensors)
3. **Electric Motors** (3 sensors)
4. **Quality Control & Cooling** (4 sensors)

Sensors update every 2 seconds by default and can be controlled through the web interface at `/sensors`.

## Running the System

### Start Backend
```bash
cd Backend
python app.py
```

### Start Frontend
```bash
cd FrontEnd
npm run dev
```

### Access the Application
- Main Dashboard: http://localhost:8080/
- Sensors Page: http://localhost:8080/sensors