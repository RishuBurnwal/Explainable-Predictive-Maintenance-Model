"""
Prediction API endpoints for RUL and failure risk predictions
"""

from flask import Blueprint, request, jsonify
import numpy as np
import pandas as pd
from datetime import datetime
import logging

from AI.model_manager import ModelManager

prediction_bp = Blueprint('prediction', __name__)
logger = logging.getLogger(__name__)

# Initialize model manager
model_manager = ModelManager()

@prediction_bp.route('/rul', methods=['POST'])
def predict_rul():
    """
    Predict Remaining Useful Life
    
    Expected input:
    {
        "sensor_data": [24 sensor values],
        "machine_id": "optional machine identifier"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'sensor_data' not in data:
            return jsonify({'error': 'Missing sensor_data in request'}), 400
        
        sensor_data = np.array(data['sensor_data'])
        machine_id = data.get('machine_id', 'unknown')
        
        # Validate input
        model_manager.validate_input_data(sensor_data)
        
        # Make prediction
        rul_prediction, metadata = model_manager.predict_rul(sensor_data)
        
        response = {
            'machine_id': machine_id,
            'rul_prediction': rul_prediction,
            'risk_level': metadata['risk_level'],
            'confidence': metadata['prediction_confidence'],
            'model_info': {
                'type': metadata['model_type'],
                'version': '2.1.0'
            },
            'timestamp': metadata['timestamp'],
            'status': 'success'
        }
        
        return jsonify(response)
        
    except ValueError as e:
        logger.warning(f"Validation error in RUL prediction: {str(e)}")
        return jsonify({'error': str(e), 'status': 'validation_error'}), 400
        
    except Exception as e:
        logger.error(f"RUL prediction failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@prediction_bp.route('/failure-risk', methods=['POST'])
def predict_failure_risk():
    """
    Predict failure risk classification
    
    Expected input:
    {
        "sensor_data": [24 sensor values],
        "machine_id": "optional machine identifier"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'sensor_data' not in data:
            return jsonify({'error': 'Missing sensor_data in request'}), 400
        
        sensor_data = np.array(data['sensor_data'])
        machine_id = data.get('machine_id', 'unknown')
        
        # Validate input
        model_manager.validate_input_data(sensor_data)
        
        # Make prediction
        risk_class, metadata = model_manager.predict_failure_risk(sensor_data)
        
        response = {
            'machine_id': machine_id,
            'risk_class': risk_class,
            'probabilities': metadata['probabilities'],
            'confidence': metadata['confidence'],
            'model_info': {
                'type': metadata['model_type'],
                'version': '2.1.0'
            },
            'timestamp': metadata['timestamp'],
            'status': 'success'
        }
        
        return jsonify(response)
        
    except ValueError as e:
        logger.warning(f"Validation error in failure risk prediction: {str(e)}")
        return jsonify({'error': str(e), 'status': 'validation_error'}), 400
        
    except Exception as e:
        logger.error(f"Failure risk prediction failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@prediction_bp.route('/batch', methods=['POST'])
def batch_predict():
    """
    Batch predictions for multiple machines
    
    Expected input:
    {
        "machines": [
            {
                "machine_id": "MACHINE-001",
                "sensor_data": [24 sensor values]
            },
            ...
        ],
        "prediction_types": ["rul", "failure_risk", "anomaly"]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'machines' not in data:
            return jsonify({'error': 'Missing machines data in request'}), 400
        
        machines = data['machines']
        prediction_types = data.get('prediction_types', ['rul', 'failure_risk'])
        
        results = []
        
        for machine in machines:
            machine_id = machine.get('machine_id', 'unknown')
            sensor_data = np.array(machine['sensor_data'])
            
            try:
                # Validate input
                model_manager.validate_input_data(sensor_data)
                
                machine_result = {
                    'machine_id': machine_id,
                    'predictions': {},
                    'status': 'success'
                }
                
                # RUL prediction
                if 'rul' in prediction_types:
                    rul_pred, rul_meta = model_manager.predict_rul(sensor_data)
                    machine_result['predictions']['rul'] = {
                        'value': rul_pred,
                        'risk_level': rul_meta['risk_level'],
                        'confidence': rul_meta['prediction_confidence']
                    }
                
                # Failure risk prediction
                if 'failure_risk' in prediction_types:
                    risk_class, risk_meta = model_manager.predict_failure_risk(sensor_data)
                    machine_result['predictions']['failure_risk'] = {
                        'class': risk_class,
                        'probabilities': risk_meta['probabilities'],
                        'confidence': risk_meta['confidence']
                    }
                
                # Anomaly detection
                if 'anomaly' in prediction_types:
                    is_anomaly, anomaly_meta = model_manager.detect_anomaly(sensor_data)
                    machine_result['predictions']['anomaly'] = {
                        'is_anomaly': is_anomaly,
                        'score': anomaly_meta['anomaly_score'],
                        'confidence': anomaly_meta['confidence']
                    }
                
                results.append(machine_result)
                
            except Exception as e:
                logger.warning(f"Prediction failed for machine {machine_id}: {str(e)}")
                results.append({
                    'machine_id': machine_id,
                    'error': str(e),
                    'status': 'error'
                })
        
        response = {
            'results': results,
            'total_machines': len(machines),
            'successful_predictions': len([r for r in results if r['status'] == 'success']),
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'completed'
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Batch prediction failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@prediction_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for prediction service"""
    try:
        models_status = model_manager.get_models_status()
        
        return jsonify({
            'service': 'Prediction API',
            'status': 'healthy',
            'models': models_status,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'service': 'Prediction API',
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500
