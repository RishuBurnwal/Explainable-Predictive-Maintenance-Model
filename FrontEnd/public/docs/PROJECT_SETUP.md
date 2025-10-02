# 🚀 Project Setup Guide

## 📁 Complete Project Structure

```
Explainable Predictive Maintenance Model/
├── setup_manager.py                     # 🆕 Universal Setup Manager
├── setup.bat                           # 🆕 Windows launcher
├── setup.sh                            # 🆕 Linux launcher  
├── SETUP_README.md                     # 🆕 Setup documentation
├── QUICK_START.md                      # 🆕 Quick start guide
├── FrontEnd/                            # React TypeScript Frontend
│   ├── public/
│   │   ├── docs/                        # Documentation files
│   │   │   ├── README.md                # Project overview
│   │   │   ├── PROJECT_SUMMARY.md       # Complete documentation
│   │   │   ├── PROJECT_SETUP.md         # Setup guide
│   │   │   ├── FAQ.md                   # Troubleshooting
│   │   │   ├── DEPLOYMENT.md            # Production guide
│   │   │   └── LICENSE.md               # License terms
│   │   ├── favicon.ico
│   │   └── placeholder.svg
│   ├── src/
│   │   ├── components/                  # UI Components
│   │   │   ├── Navigation.tsx           # Main navigation
│   │   │   ├── Hero.tsx                 # Landing hero section
│   │   │   ├── StatusCard.tsx           # Real-time status cards
│   │   │   ├── DataVisualization.tsx    # Interactive charts
│   │   │   ├── ExplainabilityPanel.tsx  # SHAP/LIME visualizations
│   │   │   ├── AlertCard.tsx            # Alert notifications
│   │   │   ├── DashboardSidebar.tsx     # Filters panel
│   │   │   ├── ErrorBoundary.tsx        # Error handling
│   │   │   └── ui/                      # Shadcn/ui components
│   │   │       ├── button.tsx
│   │   │       ├── card.tsx
│   │   │       ├── badge.tsx
│   │   │       ├── tabs.tsx
│   │   │       └── [30+ UI components]
│   │   ├── pages/
│   │   │   ├── Index.tsx                # Main dashboard
│   │   │   ├── Documentation.tsx        # Documentation viewer
│   │   │   └── NotFound.tsx             # 404 page
│   │   ├── lib/
│   │   │   ├── api.ts                   # TypeScript API client
│   │   │   ├── dataset.ts               # Dataset utilities
│   │   │   └── utils.ts                 # Utility functions
│   │   ├── hooks/
│   │   │   ├── use-mobile.tsx           # Mobile detection
│   │   │   └── use-toast.ts             # Toast notifications
│   │   ├── App.tsx                      # Main React app
│   │   ├── main.tsx                     # Entry point
│   │   └── index.css                    # Global styles
│   ├── package.json                     # Dependencies and scripts
│   ├── vite.config.ts                   # Vite configuration
│   ├── tailwind.config.ts               # Tailwind CSS config
│   └── tsconfig.json                    # TypeScript config
│
├── Backend/                             # Flask Python Backend
│   ├── AI/                              # AI Models and Logic
│   │   ├── __init__.py
│   │   ├── model_manager.py             # Model loading/management
│   │   ├── pretrained_models.py         # Model training scripts
│   │   └── explainability.py           # SHAP/LIME implementations
│   ├── api/                             # REST API Endpoints
│   │   ├── __init__.py
│   │   ├── prediction_api.py            # RUL/failure predictions
│   │   ├── explainability_api.py        # SHAP/LIME endpoints
│   │   ├── anomaly_api.py               # Anomaly detection
│   │   └── data_api.py                  # Data management
│   ├── data/                            # Data Management
│   │   ├── sample_turbofan_data.py      # Dataset generator
│   │   └── sample_datasets/             # Generated CSV files
│   │       ├── turbofan_data_small.csv  # 500 samples
│   │       ├── turbofan_data_medium.csv # 4,000 samples
│   │       ├── turbofan_data_large.csv  # 15,000 samples
│   │       ├── turbofan_train_*.csv     # Training sets
│   │       └── turbofan_test_*.csv      # Test sets
│   ├── models/                          # Saved AI Models
│   │   ├── rul_xgboost_model.pkl        # RUL prediction model
│   │   ├── failure_lgb_model.pkl        # Failure classification
│   │   ├── anomaly_isolation_forest.pkl # Anomaly detection
│   │   ├── rul_scaler.pkl               # Feature scalers
│   │   ├── failure_scaler.pkl
│   │   └── anomaly_scaler.pkl
│   ├── utils/                           # Utilities
│   │   ├── __init__.py
│   │   ├── config.py                    # Configuration
│   │   └── logger.py                    # Logging setup
│   ├── logs/                            # Application logs
│   ├── temp/                            # Temporary files
│   ├── app.py                           # Main Flask application
│   ├── setup.py                         # Setup script
│   ├── test_api.py                      # API tests
│   ├── frontend_integration.js          # JS integration helper
│   ├── requirements.txt                 # Python dependencies
│   ├── .env                             # Environment variables
│   ├── start_server.bat                 # Windows startup
│   ├── start_server.sh                  # Unix startup
│   └── README.md                        # Backend documentation
│
├── models/                              # Pre-trained Models (backup)
├── documentation/                       # Additional docs
├── PROJECT_SUMMARY.md                   # Project overview
└── LICENSE                              # MIT License
```

## 🛠️ Installation & Setup

### Prerequisites

Before starting, ensure you have:

- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download here](https://python.org/)
- **Git** (optional) - [Download here](https://git-scm.com/)

### Step 1: Backend Setup

```bash
# Navigate to Backend directory
cd Backend

# Run automated setup (recommended)
python setup.py

# OR Manual setup:
# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir models data/sample_datasets logs temp

# Generate sample data
python data/sample_turbofan_data.py

# Create and train models
python AI/pretrained_models.py

# Start the backend server
python app.py
```

**Backend will be available at:** `http://localhost:5000`

### Step 2: Frontend Setup

```bash
# Navigate to Frontend directory
cd FrontEnd

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend will be available at:** `http://localhost:8080`

### Step 3: Verification

1. **Backend Health Check:**
   ```bash
   curl http://localhost:5000/api/v1/status
   ```

2. **Frontend Access:**
   - Open browser to `http://localhost:8080`
   - Check connection status in the dashboard

## ⚙️ Configuration

### Backend Configuration

**Environment Variables (`.env`):**
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

**Model Configuration (`utils/config.py`):**
- Model file paths and types
- Feature definitions and names
- Threshold settings for predictions
- API limits and timeouts

### Frontend Configuration

**Vite Configuration (`vite.config.ts`):**
```typescript
export default defineConfig(() => ({
  server: {
    host: "::",
    port: 8080,  // Frontend port
  },
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
}));
```

**API Configuration (`src/lib/api.ts`):**
```typescript
const API_BASE_URL = 'http://localhost:5000/api/v1';
```

## 📊 Sample Datasets

The system includes three pre-generated NASA Turbofan-inspired datasets:

### Dataset Specifications

| Dataset | Size | Engines | Cycles | Features | Use Case |
|---------|------|---------|---------|----------|----------|
| **Small** | 500 samples | 5 | 100 each | 24 sensors | Development/Testing |
| **Medium** | 4,000 samples | 20 | 200 each | 24 sensors | Training/Validation |
| **Large** | 15,000 samples | 50 | 300 each | 24 sensors | Production/Research |

### Feature Set (24 total)

**Operational Settings (3):**
- Altitude (normalized)
- Mach number (normalized) 
- Throttle angle (normalized)

**Sensor Measurements (21):**
- Temperature sensors (T1-T7)
- Pressure sensors (P1-P5)
- Speed sensors (N1-N3)
- Flow sensors (F1-F6)

### Target Variables

- **RUL (Remaining Useful Life):** Continuous value in cycles/hours
- **Failure Risk:** Categorical (Low/Medium/High)
- **Anomaly Score:** Continuous value (0-1)

## 🔌 API Integration

### Key Endpoints

```bash
# Health & Status
GET  /                              # Basic health check
GET  /api/v1/status                 # Detailed status

# Predictions
POST /api/v1/prediction/rul         # RUL prediction
POST /api/v1/prediction/failure-risk # Risk classification
POST /api/v1/prediction/batch       # Batch predictions

# Explainability
POST /api/v1/explainability/shap    # SHAP explanations
POST /api/v1/explainability/lime    # LIME explanations
GET  /api/v1/explainability/feature-importance # Global importance

# Anomaly Detection
POST /api/v1/anomaly/detect         # Single anomaly check
POST /api/v1/anomaly/batch-detect   # Batch anomaly detection

# Data Management
POST /api/v1/data/generate-sample   # Generate test data
POST /api/v1/data/validate          # Validate sensor data
```

### Frontend API Client Usage

```typescript
import { usePredictiveMaintenanceAPI, generateSampleSensorData } from '@/lib/api';

const { api, testConnection, getCompletePrediction } = usePredictiveMaintenanceAPI();

// Test connection
const status = await testConnection();

// Get predictions
const sensorData = generateSampleSensorData();
const prediction = await getCompletePrediction(sensorData, 'MACHINE-001');

// Individual predictions
const rul = await api.predictRUL(sensorData, 'MACHINE-001');
const risk = await api.predictFailureRisk(sensorData, 'MACHINE-001');
const anomaly = await api.detectAnomaly(sensorData, 'MACHINE-001');

// Explainability
const shap = await api.getSHAPExplanation(sensorData, 'rul', 10);
const lime = await api.getLIMEExplanation(sensorData, 'failure', 10);
```

## 🚀 Deployment

### Development
```bash
# Backend
cd Backend && python app.py

# Frontend  
cd FrontEnd && npm run dev
```

### Production

**Frontend:**
```bash
npm run build
# Serve dist/ folder with nginx/Apache
```

**Backend:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🧪 Testing

### Backend Testing
```bash
cd Backend
python test_api.py
```

### Frontend Testing
```bash
cd FrontEnd
npm run test
```

### Manual Testing
1. Check health endpoints
2. Test predictions with sample data
3. Verify explainability responses
4. Test anomaly detection
5. Validate frontend-backend integration

## 📝 Development Guidelines

### Adding New Features

1. **Backend API Endpoint:**
   - Add route in appropriate `api/` file
   - Update API documentation
   - Add tests

2. **Frontend Component:**
   - Create in `src/components/`
   - Add TypeScript interfaces
   - Connect to API

3. **AI Model:**
   - Add model logic in `AI/`
   - Update model manager
   - Create training script

### Code Style

- **Frontend:** TypeScript, Tailwind CSS, shadcn/ui
- **Backend:** Python with type hints, PEP 8
- **Documentation:** Markdown with GitHub formatting

## 🔧 Troubleshooting

### Common Issues

1. **Port conflicts:** Change ports in config files
2. **CORS errors:** Update CORS_ORIGINS in backend
3. **Model loading fails:** Run `python setup.py` again
4. **Frontend won't start:** Clear node_modules and reinstall
5. **API connection fails:** Check backend is running on port 5000

### Debug Mode

Enable detailed logging:
```bash
# Backend
export FLASK_DEBUG=True
export LOG_LEVEL=DEBUG

# Frontend
npm run dev -- --debug
```

## 📞 Support

For issues:
1. Check console logs (browser/terminal)
2. Verify both servers are running
3. Test API endpoints individually
4. Check network connectivity

---

🎉 **You're all set!** The Explainable Predictive Maintenance system should now be running with full functionality.
