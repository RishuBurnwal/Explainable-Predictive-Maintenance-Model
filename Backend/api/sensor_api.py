"""
Sensor API endpoints for IoT sensor management
Provides real-time sensor data and control
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
import logging

from AI.sensor_manager import get_sensor_manager
from AI.model_manager import ModelManager

sensor_bp = Blueprint('sensor', __name__)
logger = logging.getLogger(__name__)

# Initialize managers
sensor_manager = get_sensor_manager()
model_manager = ModelManager()

@sensor_bp.route('/sensors', methods=['GET'])
def get_all_sensors():
    """
    Get all sensors in the factory
    
    Query params:
        active_only: bool - Return only active sensors
    """
    try:
        active_only = request.args.get('active_only', 'false').lower() == 'true'
        
        if active_only:
            sensors = sensor_manager.get_active_sensors()
        else:
            sensors = sensor_manager.get_all_sensors()
        
        return jsonify({
            'sensors': sensors,
            'count': len(sensors),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Failed to get sensors: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500


@sensor_bp.route('/sensors/<sensor_id>', methods=['GET'])
def get_sensor(sensor_id: str):
    """Get specific sensor details"""
    try:
        sensor = sensor_manager.get_sensor(sensor_id)
        
        if not sensor:
            return jsonify({'error': 'Sensor not found', 'status': 'error'}), 404
        
        return jsonify({
            'sensor': sensor,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Failed to get sensor {sensor_id}: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500


@sensor_bp.route('/sensors/<sensor_id>/toggle', methods=['POST'])
def toggle_sensor(sensor_id: str):
    """
    Toggle sensor active state
    
    Request body:
    {
        "is_active": true/false
    }
    """
    try:
        data = request.get_json()
        
        if 'is_active' not in data:
            return jsonify({'error': 'Missing is_active in request', 'status': 'error'}), 400
        
        is_active = data['is_active']
        success = sensor_manager.toggle_sensor(sensor_id, is_active)
        
        if not success:
            return jsonify({'error': 'Sensor not found', 'status': 'error'}), 404
        
        sensor = sensor_manager.get_sensor(sensor_id)
        
        return jsonify({
            'message': f"Sensor {'activated' if is_active else 'deactivated'}",
            'sensor': sensor,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Failed to toggle sensor {sensor_id}: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500


@sensor_bp.route('/sensors/<sensor_id>/age', methods=['POST'])
def set_sensor_age(sensor_id: str):
    """
    Set sensor age/degradation percentage
    
    Request body:
    {
        "age_percentage": 0-100
    }
    """
    try:
        data = request.get_json()
        
        if 'age_percentage' not in data:
            return jsonify({'error': 'Missing age_percentage in request', 'status': 'error'}), 400
        
        age_percentage = int(data['age_percentage'])
        
        if not (0 <= age_percentage <= 100):
            return jsonify({'error': 'age_percentage must be between 0 and 100', 'status': 'error'}), 400
        
        success = sensor_manager.set_sensor_age(sensor_id, age_percentage)
        
        if not success:
            return jsonify({'error': 'Sensor not found', 'status': 'error'}), 404
        
        sensor = sensor_manager.get_sensor(sensor_id)
        
        return jsonify({
            'message': f"Sensor age set to {age_percentage}%",
            'sensor': sensor,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'status': 'success'
        })
        
    except ValueError:
        return jsonify({'error': 'age_percentage must be an integer', 'status': 'error'}), 400
    except Exception as e:
        logger.error(f"Failed to set sensor age {sensor_id}: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500


@sensor_bp.route('/sensors/statistics', methods=['GET'])
def get_sensor_statistics():
    """Get sensor network statistics"""
    try:
        stats = sensor_manager.get_statistics()
        
        return jsonify({
            'statistics': stats,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Failed to get statistics: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500


@sensor_bp.route('/sensors/realtime-data', methods=['GET'])
def get_realtime_sensor_data():
    """
    Get current real-time data from all active sensors
    Formatted for visualization
    """
    try:
        sensors = sensor_manager.get_active_sensors()
        
        # Group sensors by type
        sensor_groups = {}
        for sensor in sensors:
            sensor_type = sensor['type']
            if sensor_type not in sensor_groups:
                sensor_groups[sensor_type] = []
            sensor_groups[sensor_type].append(sensor)
        
        return jsonify({
            'sensors': sensors,
            'grouped_by_type': sensor_groups,
            'count': len(sensors),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Failed to get real-time data: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500


@sensor_bp.route('/sensors/predict', methods=['POST'])
def predict_from_sensors():
    """
    Generate AI predictions based on current sensor data
    
    Request body (optional):
    {
        "prediction_types": ["rul", "failure_risk", "anomaly"]
    }
    """
    try:
        data = request.get_json() or {}
        prediction_types = data.get('prediction_types', ['rul', 'failure_risk', 'anomaly'])
        
        # Get aggregated sensor data
        sensor_data = sensor_manager.get_sensor_data_for_prediction()
        
        # Validate input
        model_manager.validate_input_data(sensor_data)
        
        predictions = {}
        
        # RUL prediction
        if 'rul' in prediction_types:
            rul_pred, rul_meta = model_manager.predict_rul(sensor_data)
            predictions['rul'] = {
                'value': rul_pred,
                'risk_level': rul_meta['risk_level'],
                'confidence': rul_meta['prediction_confidence'],
                'unit': 'hours'
            }
        
        # Failure risk prediction
        if 'failure_risk' in prediction_types:
            risk_class, risk_meta = model_manager.predict_failure_risk(sensor_data)
            predictions['failure_risk'] = {
                'class': risk_class,
                'probabilities': risk_meta['probabilities'],
                'confidence': risk_meta['confidence']
            }
        
        # Anomaly detection
        if 'anomaly' in prediction_types:
            is_anomaly, anomaly_meta = model_manager.detect_anomaly(sensor_data)
            predictions['anomaly'] = {
                'is_anomaly': is_anomaly,
                'score': anomaly_meta['anomaly_score'],
                'confidence': anomaly_meta['confidence']
            }
        
        # Get sensor statistics
        sensor_stats = sensor_manager.get_statistics()
        
        return jsonify({
            'predictions': predictions,
            'sensor_stats': sensor_stats,
            'active_sensors': sensor_stats['active_sensors'],
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'status': 'success'
        })
        
    except ValueError as e:
        logger.warning(f"Validation error in sensor prediction: {str(e)}")
        return jsonify({'error': str(e), 'status': 'validation_error'}), 400
        
    except Exception as e:
        logger.error(f"Sensor prediction failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500


@sensor_bp.route('/sensors/health', methods=['GET'])
def get_sensor_health():
    """Get overall sensor network health status"""
    try:
        stats = sensor_manager.get_statistics()
        sensors = sensor_manager.get_all_sensors()
        
        # Categorize sensors by status
        critical_sensors = [s for s in sensors if s['status'] == 'critical']
        warning_sensors = [s for s in sensors if s['status'] == 'warning']
        
        health_status = 'healthy'
        if stats['critical_sensors'] > 0:
            health_status = 'critical'
        elif stats['warning_sensors'] > 3:
            health_status = 'warning'
        
        return jsonify({
            'health_status': health_status,
            'statistics': stats,
            'critical_sensors': critical_sensors,
            'warning_sensors': warning_sensors,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Failed to get sensor health: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500


@sensor_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for sensor service"""
    try:
        stats = sensor_manager.get_statistics()
        
        return jsonify({
            'service': 'Sensor API',
            'status': 'healthy',
            'sensor_network': stats,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'service': 'Sensor API',
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 500
