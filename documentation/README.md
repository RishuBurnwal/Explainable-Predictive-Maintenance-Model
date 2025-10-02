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
│   │   │   └── ExplainabilityPanel.tsx
│   │   ├── pages/
│   │   │   ├── Index.tsx
│   │   │   ├── Documentation.tsx
│   │   │   └── ...
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── assets/
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── README.md
├── Backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── models/
│   ├── routes/
│   └── utils/
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
└── documentation/
    ├── README.md
    └── LICENSE
```

## Getting Started

### Prerequisites
- Node.js (v16 or later)
- Python (v3.8 or later)
- npm or yarn

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

## Features

- Real-time equipment monitoring
- Predictive maintenance alerts
- Explainable AI insights
- Interactive data visualization
- Historical data analysis

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
