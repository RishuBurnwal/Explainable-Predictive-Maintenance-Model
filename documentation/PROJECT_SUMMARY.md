# Project Summary

## Overview
The Explainable Predictive Maintenance Model is a comprehensive solution designed to predict equipment failures and provide interpretable insights into the predictions. This system combines machine learning with explainable AI techniques to help maintenance teams make data-driven decisions. It now includes a complete IoT sensor network with real-time monitoring capabilities.

## Key Features

### 1. Real-time Monitoring
- Continuous equipment monitoring with live data feeds
- Real-time health status visualization
- Alert system for abnormal conditions
- IoT sensor network with 16 industrial sensors

### 2. Predictive Analytics
- Machine learning models for failure prediction
- Remaining useful life estimation
- Anomaly detection in equipment behavior

### 3. Explainable AI
- Model interpretability with SHAP values
- Feature importance visualization
- What-if analysis for different scenarios

### 4. Data Visualization
- Interactive dashboards
- Historical trend analysis
- Performance metrics and KPIs

### 5. IoT Sensor Integration
- 16 industrial sensors across 4 production lines
- Real-time sensor data streaming
- Sensor activation/deactivation controls
- Health status monitoring

## Technology Stack

### Frontend
- React with TypeScript
- Vite for build tooling
- Shadcn UI components
- Recharts for data visualization

### Backend
- Python with FastAPI
- XGBoost for predictive modeling
- SHAP for model explainability
- SQLite/PostgreSQL for data storage

### MLOps
- Model versioning with DVC
- Experiment tracking with MLflow
- Automated model retraining

### IoT Integration
- Real-time sensor simulation
- Sensor data processing pipeline
- REST API for sensor management