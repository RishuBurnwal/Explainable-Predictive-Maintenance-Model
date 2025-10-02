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
```

2. Update the frontend configuration in `FrontEnd/vite.config.ts` if needed.
