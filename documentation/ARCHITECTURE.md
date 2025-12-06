# System Architecture

## High-Level Architecture

The system follows a modern web application architecture with clear separation of concerns between the frontend, backend, and IoT sensor network components.

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

## Component Breakdown

### 1. Frontend Layer
- **React Application**: Single Page Application (SPA) built with React and TypeScript
- **State Management**: React Context API with useReducer
- **UI Components**: Built with Shadcn UI and Tailwind CSS
- **Data Visualization**: Recharts for interactive charts and graphs
- **IoT Dashboard**: Dedicated sensor monitoring page with real-time updates
- **Routing**: React Router for client-side navigation
- **API Client**: Custom TypeScript API client for backend communication

### 2. Backend Layer
- **API Framework**: Flask for handling HTTP requests
- **Endpoints**:
  - `/api/v1/prediction/*` - For making predictions (RUL, failure risk)
  - `/api/v1/explainability/*` - For model explanations (SHAP, LIME)
  - `/api/v1/anomaly/*` - For anomaly detection
  - `/api/v1/data/*` - For data management
  - `/api/v1/sensors/*` - For IoT sensor management
- **CORS**: Enabled for cross-origin requests from frontend
- **Logging**: Structured logging for monitoring and debugging

### 3. Machine Learning Layer
- **Model Orchestration**: ModelManager for loading and managing ML models
- **RUL Prediction**: XGBoost regressor for Remaining Useful Life estimation
- **Failure Classification**: LightGBM classifier for risk assessment
- **Anomaly Detection**: Isolation Forest for unsupervised anomaly identification
- **Explainability**: SHAP and LIME for model interpretation
- **Model Persistence**: Joblib for model serialization

### 4. IoT Sensor Layer
- **Sensor Network**: 16 industrial sensors across 4 production lines
- **Real-time Processing**: Live data streaming and processing every 2 seconds
- **Sensor Management**: Activation/deactivation controls with toggle switches
- **Health Monitoring**: Status tracking with Normal, Warning, Critical indicators
- **Age Simulation**: Adjustable sensor degradation settings (0-100%)
- **Data Aggregation**: Sensor data formatting for ML model input

## Data Flow

1. **IoT Sensor Network**
   - 16 industrial sensors continuously monitor equipment
   - Real-time data collection every 2 seconds
   - Sensor health status tracking (Normal, Warning, Critical)
   - Toggle controls for sensor activation/deactivation

2. **Data Ingestion**
   - Collect sensor data from IoT network
   - Real-time processing and validation
   - Data normalization and feature engineering
   - Format conversion for ML model input (24-feature vectors)

3. **Model Serving**
   - REST API for model inference
   - Real-time prediction processing
   - Batch prediction support for multiple machines
   - Confidence scoring and risk assessment

4. **Explanation Service**
   - SHAP values calculation for global feature importance
   - LIME explanations for local interpretability
   - Feature importance visualization
   - Risk factor analysis

5. **Frontend Presentation**
   - Real-time dashboard updates
   - Interactive charts and visualizations
   - Sensor network status monitoring
   - Alert notifications and system health indicators

## Scalability

- **Horizontal Scaling**: Stateless API services for easy scaling
- **Asynchronous Processing**: Background tasks for CPU-intensive operations
- **Efficient Resource Usage**: Optimized ML model inference
- **Modular Design**: Component-based architecture for easy extension

## Security

- **Input Validation**: Comprehensive data sanitization and validation
- **Error Handling**: Graceful failure management with proper HTTP status codes
- **CORS Protection**: Controlled cross-origin resource sharing
- **API Versioning**: Structured endpoint versioning (/api/v1/)
- **Rate Limiting**: Built-in request throttling (via Flask configuration)

## Deployment Architecture

### Development
- **Frontend**: Vite development server (port 8080)
- **Backend**: Flask development server (port 5000)
- **Communication**: Direct REST API calls between frontend and backend

### Production
- **Frontend**: Static build served by nginx or similar web server
- **Backend**: WSGI server (Gunicorn) for production deployment
- **Reverse Proxy**: nginx for SSL termination and load balancing
- **Process Management**: Supervisor or systemd for service management

## Technology Stack

### Frontend
- React 18 + TypeScript
- Vite for build tooling
- TailwindCSS for styling
- Shadcn/ui for components
- Recharts for data visualization
- React Router for navigation

### Backend
- Flask for REST API
- Python 3.8+
- XGBoost, LightGBM, Scikit-learn for ML
- SHAP, LIME for explainability
- NumPy, Pandas for data processing
- Joblib for model persistence

### Infrastructure
- Cross-platform compatibility (Windows, Linux, macOS)
- Universal setup manager for easy deployment
- Git for version control
- Standard web protocols (HTTP/HTTPS)