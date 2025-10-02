"""
Model Manager for loading and managing AI models
Handles RUL prediction, failure classification, and anomaly detection
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple
import logging
from datetime import datetime

class ModelManager:
    """Manages all AI models for predictive maintenance"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.models = {}
        self.scalers = {}
        self.model_info = {}
        self._load_all_models()
    
    def _load_all_models(self):
        """Load all available models"""
        try:
            # Load RUL Prediction Model
            self._load_rul_model()
            
            # Load Failure Classification Model
            self._load_failure_model()
            
            # Load Anomaly Detection Model
            self._load_anomaly_model()
            
            self.logger.info("All models loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error loading models: {str(e)}")
    
    def _load_rul_model(self):
        """Load RUL prediction model (XGBoost)"""
        try:
            from .pretrained_models import create_rul_model, create_rul_scaler
            
            model, scaler = create_rul_model()
            
            self.models['rul_predictor'] = model
            self.scalers['rul_scaler'] = scaler
            self.model_info['rul_predictor'] = {
                'type': 'XGBoost Regressor',
                'purpose': 'Remaining Useful Life Prediction',
                'features': 24,  # 21 sensors + 3 settings
                'loaded_at': datetime.utcnow().isoformat(),
                'status': 'ready'
            }
            
            self.logger.info("RUL prediction model loaded")
            
        except Exception as e:
            self.logger.error(f"Failed to load RUL model: {str(e)}")
            self.model_info['rul_predictor'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _load_failure_model(self):
        """Load failure classification model (LightGBM)"""
        try:
            from .pretrained_models import create_failure_model, create_failure_scaler
            
            model, scaler = create_failure_model()
            
            self.models['failure_classifier'] = model
            self.scalers['failure_scaler'] = scaler
            self.model_info['failure_classifier'] = {
                'type': 'LightGBM Classifier',
                'purpose': 'Failure Risk Classification',
                'classes': ['Low Risk', 'Medium Risk', 'High Risk'],
                'features': 24,
                'loaded_at': datetime.utcnow().isoformat(),
                'status': 'ready'
            }
            
            self.logger.info("Failure classification model loaded")
            
        except Exception as e:
            self.logger.error(f"Failed to load failure model: {str(e)}")
            self.model_info['failure_classifier'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _load_anomaly_model(self):
        """Load anomaly detection model (Isolation Forest)"""
        try:
            from .pretrained_models import create_anomaly_model, create_anomaly_scaler
            
            model, scaler = create_anomaly_model()
            
            self.models['anomaly_detector'] = model
            self.scalers['anomaly_scaler'] = scaler
            self.model_info['anomaly_detector'] = {
                'type': 'Isolation Forest',
                'purpose': 'Anomaly Detection',
                'features': 24,
                'loaded_at': datetime.utcnow().isoformat(),
                'status': 'ready'
            }
            
            self.logger.info("Anomaly detection model loaded")
            
        except Exception as e:
            self.logger.error(f"Failed to load anomaly model: {str(e)}")
            self.model_info['anomaly_detector'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def predict_rul(self, sensor_data: np.ndarray) -> Tuple[float, Dict[str, Any]]:
        """
        Predict Remaining Useful Life
        
        Args:
            sensor_data: Array of sensor readings [24 features]
            
        Returns:
            Tuple of (rul_prediction, metadata)
        """
        try:
            if 'rul_predictor' not in self.models:
                raise ValueError("RUL model not available")
            
            # Preprocess data
            scaled_data = self.scalers['rul_scaler'].transform(sensor_data.reshape(1, -1))
            
            # Make prediction
            rul_prediction = self.models['rul_predictor'].predict(scaled_data)[0]
            
            # Determine risk level
            if rul_prediction < 30:
                risk_level = "High"
            elif rul_prediction < 100:
                risk_level = "Medium"
            else:
                risk_level = "Low"
            
            metadata = {
                'model_type': 'XGBoost',
                'prediction_confidence': min(0.95, max(0.6, 1.0 - abs(rul_prediction - 100) / 200)),
                'risk_level': risk_level,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            return float(rul_prediction), metadata
            
        except Exception as e:
            self.logger.error(f"RUL prediction failed: {str(e)}")
            raise
    
    def predict_failure_risk(self, sensor_data: np.ndarray) -> Tuple[str, Dict[str, Any]]:
        """
        Predict failure risk classification
        
        Args:
            sensor_data: Array of sensor readings [24 features]
            
        Returns:
            Tuple of (risk_class, metadata)
        """
        try:
            if 'failure_classifier' not in self.models:
                raise ValueError("Failure classification model not available")
            
            # Preprocess data
            scaled_data = self.scalers['failure_scaler'].transform(sensor_data.reshape(1, -1))
            
            # Make prediction
            risk_prediction = self.models['failure_classifier'].predict(scaled_data)[0]
            risk_probabilities = self.models['failure_classifier'].predict_proba(scaled_data)[0]
            
            classes = ['Low Risk', 'Medium Risk', 'High Risk']
            risk_class = classes[risk_prediction]
            
            metadata = {
                'model_type': 'LightGBM',
                'probabilities': {
                    classes[i]: float(prob) for i, prob in enumerate(risk_probabilities)
                },
                'confidence': float(max(risk_probabilities)),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            return risk_class, metadata
            
        except Exception as e:
            self.logger.error(f"Failure risk prediction failed: {str(e)}")
            raise
    
    def detect_anomaly(self, sensor_data: np.ndarray) -> Tuple[bool, Dict[str, Any]]:
        """
        Detect anomalies in sensor data
        
        Args:
            sensor_data: Array of sensor readings [24 features]
            
        Returns:
            Tuple of (is_anomaly, metadata)
        """
        try:
            if 'anomaly_detector' not in self.models:
                raise ValueError("Anomaly detection model not available")
            
            # Preprocess data
            scaled_data = self.scalers['anomaly_scaler'].transform(sensor_data.reshape(1, -1))
            
            # Make prediction (-1 for anomaly, 1 for normal)
            anomaly_prediction = self.models['anomaly_detector'].predict(scaled_data)[0]
            anomaly_score = self.models['anomaly_detector'].decision_function(scaled_data)[0]
            
            is_anomaly = bool(anomaly_prediction == -1)  # Convert numpy bool to Python bool
            
            metadata = {
                'model_type': 'Isolation Forest',
                'anomaly_score': float(anomaly_score),
                'threshold': 0.0,
                'confidence': float(abs(anomaly_score)),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            return is_anomaly, metadata
            
        except Exception as e:
            self.logger.error(f"Anomaly detection failed: {str(e)}")
            raise
    
    def get_models_status(self) -> Dict[str, Any]:
        """Get status of all loaded models"""
        return {
            'models': self.model_info,
            'total_models': len(self.models),
            'healthy_models': len([m for m in self.model_info.values() if m.get('status') == 'ready']),
            'last_check': datetime.utcnow().isoformat()
        }
    
    def validate_input_data(self, data: np.ndarray) -> bool:
        """Validate input data format"""
        if data.shape[-1] != 24:
            raise ValueError(f"Expected 24 features, got {data.shape[-1]}")
        
        if np.any(np.isnan(data)) or np.any(np.isinf(data)):
            raise ValueError("Input data contains NaN or infinite values")
        
        return True
