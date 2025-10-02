"""
Configuration settings for the Predictive Maintenance API
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Model settings
    MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    AI_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'AI')
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    
    # API settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Model configuration
    MODELS = {
        'rul_predictor': {
            'type': 'xgboost',
            'file': 'rul_xgboost_model.pkl',
            'scaler': 'rul_scaler.pkl'
        },
        'failure_classifier': {
            'type': 'lightgbm',
            'file': 'failure_lgb_model.pkl',
            'scaler': 'failure_scaler.pkl'
        },
        'anomaly_detector': {
            'type': 'isolation_forest',
            'file': 'anomaly_isolation_forest.pkl',
            'scaler': 'anomaly_scaler.pkl'
        }
    }
    
    # Feature configuration
    SENSOR_FEATURES = [
        'sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5',
        'sensor_6', 'sensor_7', 'sensor_8', 'sensor_9', 'sensor_10',
        'sensor_11', 'sensor_12', 'sensor_13', 'sensor_14', 'sensor_15',
        'sensor_16', 'sensor_17', 'sensor_18', 'sensor_19', 'sensor_20',
        'sensor_21'
    ]
    
    OPERATIONAL_SETTINGS = [
        'setting_1', 'setting_2', 'setting_3'
    ]
    
    # Thresholds
    RUL_CRITICAL_THRESHOLD = 30  # cycles
    RUL_WARNING_THRESHOLD = 100  # cycles
    ANOMALY_THRESHOLD = 0.5
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'predictive_maintenance.log')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for production environment")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
