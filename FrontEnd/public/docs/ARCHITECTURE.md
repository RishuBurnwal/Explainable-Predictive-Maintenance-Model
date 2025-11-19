# 🏗️ System Architecture

## 👨‍💻 **Designed by Rishu Burnwal**
**Full Stack AI/ML Engineer | System Architect**

- 📧 **Email**: [rishu.burnwal@gmail.com](mailto:rishu.burnwal@gmail.com)
- 🔗 **LinkedIn**: [linkedin.com/in/rishu-burnwal](https://linkedin.com/in/rishu-burnwal)
- 🐙 **GitHub**: [github.com/rishuburnwal](https://github.com/rishuburnwal)

---

## Overview

The Explainable Predictive Maintenance Model, architected by **Rishu Burnwal**, is built on a modern, scalable architecture that combines React frontend with Flask backend and advanced AI models.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                         │
│               React TypeScript Frontend (Port 8080)            │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │   Dashboard     │ │  Visualizations │ │  Documentation  │   │
│  │   Component     │ │    Component    │ │    Component    │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                         HTTP/REST API
                                │
┌─────────────────────────────────────────────────────────────────┐
│                       API GATEWAY                              │
│                Flask Backend (Port 5000)                       │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │  Prediction API │ │ Explainability  │ │  Data API       │   │
│  │   (RUL/Risk)    │ │   API (SHAP)    │ │  (Management)   │   │
│  │  Sensor API     │ │                 │ │                 │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                         Python Objects
                                │
┌─────────────────────────────────────────────────────────────────┐
│                      AI MODELS LAYER                           │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │    XGBoost      │ │    LightGBM     │ │ Isolation Forest│   │
│  │ (RUL Predictor) │ │ (Risk Classifier│ │ (Anomaly Detect)│   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                         File System
                                │
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                               │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │   Turbofan      │ │   Preprocessed  │ │   Model Files   │   │
│  │   CSV Files     │ │   Features      │ │   (.pkl/.json)  │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Layer (React TypeScript)

**Technology Stack:**
- React 18 with TypeScript
- Vite build tool
- Tailwind CSS + Shadcn/ui
- React Router DOM
- TanStack Query
- Recharts for visualization
- React Markdown for documentation

**Key Components:**
- **Navigation.tsx**: Main navigation with responsive design
- **Hero.tsx**: Landing page hero section
- **DataVisualization.tsx**: Real-time charts and graphs
- **ExplainabilityPanel.tsx**: SHAP/LIME visualizations
- **StatusCard.tsx**: Real-time system metrics
- **Documentation.tsx**: GitHub-style documentation viewer
- **Sensors.tsx**: IoT sensor monitoring dashboard
- **DashboardSidebar.tsx**: Navigation sidebar

**Features:**
- Responsive design (mobile-first)
- Real-time data updates
- Interactive visualizations
- Error boundaries
- Loading states
- Toast notifications
- IoT sensor integration and control

### Backend Layer (Flask Python)

**Technology Stack:**
- Flask web framework
- Flask-CORS for cross-origin requests
- Pandas for data manipulation
- NumPy for numerical operations
- Scikit-learn for preprocessing

**API Endpoints:**
```
GET  /api/v1/status              # Health check
GET  /api/v1/data/generate       # Generate sample data
POST /api/v1/data/load-dataset   # Load existing dataset
POST /api/v1/predict/rul         # RUL prediction
POST /api/v1/predict/failure     # Failure classification
POST /api/v1/anomaly/detect      # Anomaly detection
POST /api/v1/explain/shap        # SHAP explanations
POST /api/v1/explain/lime        # LIME explanations
GET  /api/v1/sensors/sensors     # Get all sensors
POST /api/v1/sensors/sensors/{id}/toggle # Toggle sensor
GET  /api/v1/sensors/sensors/statistics # Network statistics
```

**Architecture Patterns:**
- Blueprint-based modular structure
- Dependency injection for models
- Singleton pattern for model managers
- Factory pattern for data generators

### AI Models Layer

**Model Pipeline:**
1. **Data Preprocessing**: Feature scaling, normalization
2. **Feature Engineering**: Sensor fusion, temporal features
3. **Model Inference**: Parallel processing for multiple models
4. **Post-processing**: Result aggregation, confidence scoring

**Models:**
- **XGBoost Regressor**: RUL (Remaining Useful Life) prediction
- **LightGBM Classifier**: Failure type classification
- **Isolation Forest**: Anomaly detection
- **SHAP Explainer**: Global and local explanations
- **LIME Explainer**: Instance-level explanations

### Data Layer

**Dataset Structure:**
```
Sensor Data (21 features):
- sensor_1 to sensor_21: Various engine parameters
- operational_setting_1 to operational_setting_3: Operating conditions
- cycle: Time cycle number
- engine_id: Unique engine identifier
- rul: Remaining Useful Life (target variable)
```

**Data Flow:**
1. Raw sensor data ingestion
2. Feature preprocessing and scaling
3. Model inference
4. Result aggregation
5. Visualization preparation

## Communication Flow

### Data Flow Sequence

1. **Frontend Request**: User interacts with dashboard
2. **API Call**: HTTP request to Flask backend
3. **Data Processing**: Backend validates and processes request
4. **Model Inference**: AI models generate predictions
5. **Explainability**: SHAP/LIME generate explanations
6. **Response**: JSON response with results and explanations
7. **Visualization**: Frontend renders charts and insights

### Error Handling

**Frontend:**
- Error boundaries catch React errors
- API error handling with retry logic
- User-friendly error messages
- Fallback to demo data when backend unavailable

**Backend:**
- Try-catch blocks for model operations
- Structured error responses
- Logging for debugging
- Graceful degradation

## Scalability Considerations

### Performance Optimizations

**Frontend:**
- Component memoization
- Lazy loading
- Virtual scrolling for large datasets
- Debounced API calls
- Efficient state management

**Backend:**
- Model caching and reuse
- Batch processing for multiple predictions
- Connection pooling
- Asynchronous processing where possible

### Deployment Architecture

**Development:**
```
Frontend: http://localhost:8080 (Vite dev server)
Backend:  http://localhost:5000 (Flask dev server)
```

**Production:**
```
Frontend: Static files served by CDN/Web server
Backend:  Gunicorn + Nginx reverse proxy
Models:   Cached in memory with Redis backup
Data:     PostgreSQL/MongoDB for persistence
```

## Security Features

**API Security:**
- CORS configuration
- Input validation
- Error message sanitization
- Rate limiting (production)

**Data Security:**
- No sensitive data storage
- Synthetic dataset usage
- Environment variable configuration
- Secure model file handling

## Monitoring & Observability

**Logging:**
- Structured JSON logging
- Request/response tracking
- Error tracking with stack traces
- Performance metrics

**Health Checks:**
- Backend health endpoint
- Model availability checks
- Database connectivity (if applicable)
- Resource usage monitoring

## Technology Choices Rationale

**Frontend: React + TypeScript**
- Modern, component-based architecture
- Strong typing for better development experience
- Large ecosystem and community support
- Excellent tooling and debugging

**Backend: Flask**
- Lightweight and flexible
- Easy integration with Python ML libraries
- Simple deployment and scaling
- Great for MVP and rapid prototyping

**AI: Scikit-learn + XGBoost + LightGBM**
- Battle-tested ML algorithms
- Excellent performance for tabular data
- Good explainability support
- Industry standard tools

**Visualization: Recharts**
- React-native charting library
- Composable and customizable
- Good performance with streaming data
- Accessible and responsive

This architecture provides a solid foundation for a production-ready predictive maintenance system with room for future enhancements and scaling.