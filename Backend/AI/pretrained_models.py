"""
Pretrained Models for Predictive Maintenance
Creates and trains models using synthetic NASA Turbofan-like data
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
import xgboost as xgb
import lightgbm as lgb
import joblib
import os
from typing import Tuple, Any
import logging

logger = logging.getLogger(__name__)

def generate_synthetic_turbofan_data(n_samples: int = 10000) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """
    Generate synthetic turbofan engine data similar to NASA dataset
    
    Returns:
        Tuple of (features_df, rul_targets, failure_targets)
    """
    np.random.seed(42)  # For reproducibility
    
    # Generate synthetic sensor data
    data = {}
    
    # Operational settings (3 settings)
    data['setting_1'] = np.random.normal(0, 1, n_samples)
    data['setting_2'] = np.random.normal(0, 1, n_samples)
    data['setting_3'] = np.random.normal(0, 1, n_samples)
    
    # Sensor measurements (21 sensors)
    for i in range(1, 22):
        # Create correlated sensor data with some degradation patterns
        base_signal = np.random.normal(0, 1, n_samples)
        
        # Add degradation trend for some sensors
        if i in [2, 3, 4, 7, 11, 12, 15, 17, 20, 21]:
            degradation = np.linspace(0, 2, n_samples) + np.random.normal(0, 0.1, n_samples)
            base_signal += degradation
        
        # Add operational setting influence
        base_signal += 0.3 * data['setting_1'] + 0.2 * data['setting_2']
        
        data[f'sensor_{i}'] = base_signal
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Generate RUL targets (Remaining Useful Life)
    # Higher sensor values generally indicate more degradation, lower RUL
    degradation_score = (
        df['sensor_2'] + df['sensor_3'] + df['sensor_4'] + 
        df['sensor_7'] + df['sensor_11'] + df['sensor_12'] +
        df['sensor_15'] + df['sensor_17'] + df['sensor_20'] + df['sensor_21']
    ) / 10
    
    # Convert degradation to RUL (inverse relationship with noise)
    max_rul = 300
    rul_targets = max_rul - (degradation_score * 50) + np.random.normal(0, 20, n_samples)
    rul_targets = np.clip(rul_targets, 1, max_rul)  # Ensure positive RUL
    
    # Generate failure risk targets based on RUL
    failure_targets = np.zeros(n_samples)
    failure_targets[rul_targets < 50] = 2  # High risk
    failure_targets[(rul_targets >= 50) & (rul_targets < 150)] = 1  # Medium risk
    failure_targets[rul_targets >= 150] = 0  # Low risk
    
    return df, rul_targets, failure_targets.astype(int)

def create_rul_model() -> Tuple[Any, Any]:
    """
    Create and train RUL prediction model (XGBoost)
    
    Returns:
        Tuple of (trained_model, scaler)
    """
    logger.info("Creating RUL prediction model...")
    
    # Generate training data
    X, y_rul, _ = generate_synthetic_turbofan_data(8000)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_rul, test_size=0.2, random_state=42
    )
    
    # Scale features - convert to numpy arrays to avoid feature name warnings
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train.values)  # Use .values to get numpy array
    X_test_scaled = scaler.transform(X_test.values)
    
    # Train XGBoost model
    model = xgb.XGBRegressor(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate model
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    
    logger.info(f"RUL Model - Train R²: {train_score:.3f}, Test R²: {test_score:.3f}")
    
    return model, scaler

def create_failure_model() -> Tuple[Any, Any]:
    """
    Create and train failure classification model (LightGBM)
    
    Returns:
        Tuple of (trained_model, scaler)
    """
    logger.info("Creating failure classification model...")
    
    # Generate training data
    X, _, y_failure = generate_synthetic_turbofan_data(8000)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_failure, test_size=0.2, random_state=42, stratify=y_failure
    )
    
    # Scale features - convert to numpy arrays to avoid feature name warnings
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train.values)  # Use .values to get numpy array
    X_test_scaled = scaler.transform(X_test.values)
    
    # Train LightGBM model
    model = lgb.LGBMClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1,
        verbose=-1
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate model
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    
    logger.info(f"Failure Model - Train Accuracy: {train_score:.3f}, Test Accuracy: {test_score:.3f}")
    
    return model, scaler

def create_anomaly_model() -> Tuple[Any, Any]:
    """
    Create and train anomaly detection model (Isolation Forest)
    
    Returns:
        Tuple of (trained_model, scaler)
    """
    logger.info("Creating anomaly detection model...")
    
    # Generate normal training data (no anomalies for unsupervised learning)
    X_normal, _, _ = generate_synthetic_turbofan_data(6000)
    
    # Scale features - convert to numpy arrays to avoid feature name warnings
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_normal.values)  # Use .values to get numpy array
    
    # Train Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,  # Expect 10% anomalies
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_scaled)
    
    # Test with some anomalous data
    X_test_normal = X_scaled[:100]
    X_test_anomaly = X_scaled[:50] + np.random.normal(0, 3, (50, X_scaled.shape[1]))  # Add noise for anomalies
    
    normal_predictions = model.predict(X_test_normal)
    anomaly_predictions = model.predict(X_test_anomaly)
    
    normal_accuracy = np.mean(normal_predictions == 1)  # Should be mostly 1 (normal)
    anomaly_accuracy = np.mean(anomaly_predictions == -1)  # Should be mostly -1 (anomaly)
    
    logger.info(f"Anomaly Model - Normal Accuracy: {normal_accuracy:.3f}, Anomaly Detection: {anomaly_accuracy:.3f}")
    
    return model, scaler

def create_rul_scaler() -> Any:
    """Create scaler for RUL model (for consistency)"""
    X, _, _ = generate_synthetic_turbofan_data(1000)
    scaler = StandardScaler()
    scaler.fit(X)
    return scaler

def create_failure_scaler() -> Any:
    """Create scaler for failure model (for consistency)"""
    X, _, _ = generate_synthetic_turbofan_data(1000)
    scaler = StandardScaler()
    scaler.fit(X)
    return scaler

def create_anomaly_scaler() -> Any:
    """Create scaler for anomaly model (for consistency)"""
    X, _, _ = generate_synthetic_turbofan_data(1000)
    scaler = StandardScaler()
    scaler.fit(X)
    return scaler

def save_models_to_disk(models_dir: str = '../models'):
    """
    Save all trained models to disk
    
    Args:
        models_dir: Directory to save models
    """
    os.makedirs(models_dir, exist_ok=True)
    
    # Create and save RUL model
    rul_model, rul_scaler = create_rul_model()
    joblib.dump(rul_model, os.path.join(models_dir, 'rul_xgboost_model.pkl'))
    joblib.dump(rul_scaler, os.path.join(models_dir, 'rul_scaler.pkl'))
    
    # Create and save failure model
    failure_model, failure_scaler = create_failure_model()
    joblib.dump(failure_model, os.path.join(models_dir, 'failure_lgb_model.pkl'))
    joblib.dump(failure_scaler, os.path.join(models_dir, 'failure_scaler.pkl'))
    
    # Create and save anomaly model
    anomaly_model, anomaly_scaler = create_anomaly_model()
    joblib.dump(anomaly_model, os.path.join(models_dir, 'anomaly_isolation_forest.pkl'))
    joblib.dump(anomaly_scaler, os.path.join(models_dir, 'anomaly_scaler.pkl'))
    
    logger.info(f"All models saved to {models_dir}")

if __name__ == "__main__":
    # Create and save models when run directly
    save_models_to_disk()
