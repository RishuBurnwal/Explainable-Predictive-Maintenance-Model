# Explainable Predictive Maintenance Backend

A comprehensive AI-powered backend for predictive maintenance with explainable AI capabilities using SHAP and LIME.

## 🚀 Features

- **RUL Prediction**: Remaining Useful Life prediction using XGBoost
- **Failure Classification**: Multi-class failure risk assessment using LightGBM  
- **Anomaly Detection**: Unsupervised anomaly detection using Isolation Forest
- **Explainable AI**: SHAP and LIME explanations for model transparency
- **Real-time API**: RESTful API endpoints for all functionalities
- **Data Processing**: Comprehensive data validation and preprocessing
- **Sample Data**: NASA Turbofan-like synthetic datasets

## 📋 Requirements

- Python 3.8+
- Flask 2.3+
- scikit-learn 1.3+
- XGBoost 1.7+
- LightGBM 4.1+
- SHAP 0.42+
- LIME 0.2+
- pandas, numpy, scipy

## 🛠️ Quick Setup

### 1. Automatic Setup (Recommended)

```bash
# Navigate to Backend directory
cd Backend

# Run the setup script
python setup.py
```

This will:
- Install all dependencies
- Create necessary directories
- Generate sample datasets
- Create and save pretrained models
- Test model functionality
- Create startup scripts

### 2. Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir models data/sample_datasets logs temp

# Generate sample data
python data/sample_turbofan_data.py

# Create pretrained models
python AI/pretrained_models.py

# Start the server
python app.py
```

## 🏃‍♂️ Running the Server

### Option 1: Direct Python
```bash
python app.py
```

### Option 2: Startup Scripts
```bash
# Windows
start_server.bat

# Unix/Mac
./start_server.sh
```

The API will be available at: **http://localhost:5000**

## 📡 API Endpoints

### Health Check
- `GET /` - Basic health check
- `GET /api/v1/status` - Detailed API status with model information

### Prediction APIs
- `POST /api/v1/prediction/rul` - Predict Remaining Useful Life
- `POST /api/v1/prediction/failure-risk` - Predict failure risk classification
- `POST /api/v1/prediction/batch` - Batch predictions for multiple machines

### Explainability APIs
- `POST /api/v1/explainability/shap` - Get SHAP explanations
- `POST /api/v1/explainability/lime` - Get LIME explanations
- `POST /api/v1/explainability/comprehensive` - Combined SHAP + LIME analysis
- `GET /api/v1/explainability/feature-importance` - Global feature importance

### Anomaly Detection APIs
- `POST /api/v1/anomaly/detect` - Detect anomalies in sensor data
- `POST /api/v1/anomaly/batch-detect` - Batch anomaly detection
- `POST /api/v1/anomaly/trend-analysis` - Analyze anomaly trends over time

### Data Management APIs
- `POST /api/v1/data/generate-sample` - Generate synthetic turbofan data
- `POST /api/v1/data/upload` - Upload and validate CSV data
- `POST /api/v1/data/preprocess` - Preprocess sensor data
- `POST /api/v1/data/validate` - Validate sensor data format

## 📊 Sample API Usage

### RUL Prediction
```bash
curl -X POST http://localhost:5000/api/v1/prediction/rul \\
  -H "Content-Type: application/json" \\
  -d '{
    "sensor_data": [0.1, 0.2, 0.3, ...24 values...],
    "machine_id": "MACHINE-001"
  }'
```

### SHAP Explanation
```bash
curl -X POST http://localhost:5000/api/v1/explainability/shap \\
  -H "Content-Type: application/json" \\
  -d '{
    "sensor_data": [0.1, 0.2, 0.3, ...24 values...],
    "model_type": "rul",
    "max_features": 10
  }'
```

### Anomaly Detection
```bash
curl -X POST http://localhost:5000/api/v1/anomaly/detect \\
  -H "Content-Type: application/json" \\
  -d '{
    "sensor_data": [0.1, 0.2, 0.3, ...24 values...],
    "machine_id": "MACHINE-001"
  }'
```

## 🧠 AI Models

### 1. RUL Predictor (XGBoost)
- **Purpose**: Predict remaining useful life in cycles/hours
- **Input**: 24 features (3 operational settings + 21 sensors)
- **Output**: Continuous RUL value with confidence and risk level

### 2. Failure Classifier (LightGBM)
- **Purpose**: Classify failure risk level
- **Input**: 24 features (3 operational settings + 21 sensors)
- **Output**: Risk class (Low/Medium/High) with probabilities

### 3. Anomaly Detector (Isolation Forest)
- **Purpose**: Detect unusual sensor patterns
- **Input**: 24 features (3 operational settings + 21 sensors)
- **Output**: Anomaly flag with severity and confidence score

## 🔍 Explainability Features

### SHAP (SHapley Additive exPlanations)
- Global feature importance across all predictions
- Local explanations for individual predictions
- Feature impact visualization
- Decision boundary analysis

### LIME (Local Interpretable Model-agnostic Explanations)
- Local instance-based explanations
- Feature perturbation analysis
- Model-agnostic interpretability
- Human-readable explanations

## 📁 Project Structure

```
Backend/
├── AI/                          # AI models and explainability
│   ├── __init__.py
│   ├── model_manager.py         # Model loading and management
│   ├── pretrained_models.py     # Model creation and training
│   └── explainability.py       # SHAP and LIME implementations
├── api/                         # API endpoints
│   ├── __init__.py
│   ├── prediction_api.py        # Prediction endpoints
│   ├── explainability_api.py    # Explainability endpoints
│   ├── anomaly_api.py          # Anomaly detection endpoints
│   └── data_api.py             # Data management endpoints
├── data/                        # Data and datasets
│   ├── sample_turbofan_data.py  # Sample data generator
│   └── sample_datasets/         # Generated datasets
├── models/                      # Saved model files
├── utils/                       # Utilities and configuration
│   ├── __init__.py
│   ├── config.py               # Configuration settings
│   └── logger.py               # Logging setup
├── logs/                        # Application logs
├── app.py                      # Main Flask application
├── setup.py                    # Setup and initialization script
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── start_server.bat           # Windows startup script
├── start_server.sh            # Unix startup script
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
API_VERSION=v1
MODEL_DIR=models
DATA_DIR=data
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:8080,http://localhost:3000
```

### Model Configuration (utils/config.py)
- Model file paths and types
- Feature definitions
- Threshold settings
- API limits and timeouts

## 🧪 Testing

### Test API Health
```bash
curl http://localhost:5000/api/v1/status
```

### Test Predictions with Sample Data
```bash
# Generate sample data
curl -X POST http://localhost:5000/api/v1/data/generate-sample \\
  -H "Content-Type: application/json" \\
  -d '{"num_samples": 10, "format": "json"}'
```

## 🚀 Deployment

### Development
```bash
python app.py  # Runs on http://localhost:5000
```

### Production
1. Set environment variables for production
2. Use a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🔗 Frontend Integration

The backend is designed to work with the React frontend. Key integration points:

1. **CORS**: Configured for `http://localhost:8080` (Vite dev server)
2. **JSON API**: All endpoints return JSON responses
3. **Error Handling**: Consistent error response format
4. **Real-time Data**: Supports batch processing for live updates

### Frontend API Client Example
```javascript
// Predict RUL
const predictRUL = async (sensorData) => {
  const response = await fetch('http://localhost:5000/api/v1/prediction/rul', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sensor_data: sensorData })
  });
  return response.json();
};

// Get SHAP explanation
const getExplanation = async (sensorData) => {
  const response = await fetch('http://localhost:5000/api/v1/explainability/shap', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      sensor_data: sensorData,
      model_type: 'rul',
      max_features: 10
    })
  });
  return response.json();
};
```

## 📈 Performance

- **Model Loading**: ~2-3 seconds on startup
- **Prediction Latency**: <100ms per request
- **Batch Processing**: Up to 1000 samples per request
- **Memory Usage**: ~500MB with all models loaded
- **Concurrent Requests**: Supports multiple simultaneous requests

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Run `python setup.py` to install dependencies
2. **Model Loading Failed**: Check if models directory exists and contains .pkl files
3. **Port Already in Use**: Change port in app.py or kill existing process
4. **CORS Issues**: Verify frontend URL in CORS_ORIGINS configuration

### Debug Mode
Set `FLASK_DEBUG=True` in .env file for detailed error messages.

### Logs
Check `logs/predictive_maintenance.log` for detailed application logs.

## 📄 License

This project is part of the Explainable Predictive Maintenance system. See main project documentation for license information.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check application logs
4. Create an issue in the project repository
