"""
Anomaly Detection API endpoints
"""

from flask import Blueprint, request, jsonify
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging

from AI.model_manager import ModelManager

anomaly_bp = Blueprint('anomaly', __name__)
logger = logging.getLogger(__name__)

# Initialize model manager
model_manager = ModelManager()

@anomaly_bp.route('/detect', methods=['POST'])
def detect_anomaly():
    """
    Detect anomalies in sensor data
    
    Expected input:
    {
        "sensor_data": [24 sensor values],
        "machine_id": "optional machine identifier",
        "threshold": 0.5 (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'sensor_data' not in data:
            return jsonify({'error': 'Missing sensor_data in request'}), 400
        
        sensor_data = np.array(data['sensor_data'])
        machine_id = data.get('machine_id', 'unknown')
        threshold = data.get('threshold', 0.5)
        
        # Validate input
        model_manager.validate_input_data(sensor_data)
        
        # Detect anomaly
        is_anomaly, metadata = model_manager.detect_anomaly(sensor_data)
        
        # Determine severity based on anomaly score
        anomaly_score = metadata['anomaly_score']
        if abs(anomaly_score) > 2.0:
            severity = 'critical'
        elif abs(anomaly_score) > 1.0:
            severity = 'high'
        elif abs(anomaly_score) > 0.5:
            severity = 'medium'
        else:
            severity = 'low'
        
        response = {
            'machine_id': machine_id,
            'is_anomaly': is_anomaly,
            'anomaly_score': metadata['anomaly_score'],
            'severity': severity,
            'confidence': metadata['confidence'],
            'threshold_used': threshold,
            'model_info': {
                'type': metadata['model_type'],
                'version': '2.1.0'
            },
            'timestamp': metadata['timestamp'],
            'status': 'success'
        }
        
        return jsonify(response)
        
    except ValueError as e:
        logger.warning(f"Validation error in anomaly detection: {str(e)}")
        return jsonify({'error': str(e), 'status': 'validation_error'}), 400
        
    except Exception as e:
        logger.error(f"Anomaly detection failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@anomaly_bp.route('/batch-detect', methods=['POST'])
def batch_detect_anomalies():
    """
    Batch anomaly detection for multiple data points
    
    Expected input:
    {
        "data_points": [
            {
                "timestamp": "2025-01-01T12:00:00Z",
                "machine_id": "MACHINE-001",
                "sensor_data": [24 sensor values]
            },
            ...
        ],
        "threshold": 0.5 (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'data_points' not in data:
            return jsonify({'error': 'Missing data_points in request'}), 400
        
        data_points = data['data_points']
        threshold = data.get('threshold', 0.5)
        
        results = []
        anomaly_count = 0
        
        for point in data_points:
            try:
                sensor_data = np.array(point['sensor_data'])
                machine_id = point.get('machine_id', 'unknown')
                timestamp = point.get('timestamp', datetime.utcnow().isoformat())
                
                # Validate input
                model_manager.validate_input_data(sensor_data)
                
                # Detect anomaly
                is_anomaly, metadata = model_manager.detect_anomaly(sensor_data)
                
                if is_anomaly:
                    anomaly_count += 1
                
                # Determine severity
                anomaly_score = metadata['anomaly_score']
                if abs(anomaly_score) > 2.0:
                    severity = 'critical'
                elif abs(anomaly_score) > 1.0:
                    severity = 'high'
                elif abs(anomaly_score) > 0.5:
                    severity = 'medium'
                else:
                    severity = 'low'
                
                result = {
                    'machine_id': machine_id,
                    'timestamp': timestamp,
                    'is_anomaly': is_anomaly,
                    'anomaly_score': metadata['anomaly_score'],
                    'severity': severity,
                    'confidence': metadata['confidence'],
                    'status': 'success'
                }
                
                results.append(result)
                
            except Exception as e:
                logger.warning(f"Anomaly detection failed for data point: {str(e)}")
                results.append({
                    'machine_id': point.get('machine_id', 'unknown'),
                    'timestamp': point.get('timestamp', datetime.utcnow().isoformat()),
                    'error': str(e),
                    'status': 'error'
                })
        
        response = {
            'results': results,
            'summary': {
                'total_points': len(data_points),
                'anomalies_detected': anomaly_count,
                'anomaly_rate': anomaly_count / len(data_points) if data_points else 0,
                'successful_analyses': len([r for r in results if r['status'] == 'success'])
            },
            'threshold_used': threshold,
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'status': 'completed'
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Batch anomaly detection failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@anomaly_bp.route('/trend-analysis', methods=['POST'])
def analyze_anomaly_trends():
    """
    Analyze anomaly trends over time
    
    Expected input:
    {
        "time_series_data": [
            {
                "timestamp": "2025-01-01T12:00:00Z",
                "machine_id": "MACHINE-001",
                "sensor_data": [24 sensor values]
            },
            ...
        ],
        "window_size": 24 (optional, hours)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'time_series_data' not in data:
            return jsonify({'error': 'Missing time_series_data in request'}), 400
        
        time_series_data = data['time_series_data']
        window_size = data.get('window_size', 24)  # hours
        
        # Sort by timestamp
        time_series_data.sort(key=lambda x: x.get('timestamp', ''))
        
        anomaly_timeline = []
        machine_stats = {}
        
        for point in time_series_data:
            try:
                sensor_data = np.array(point['sensor_data'])
                machine_id = point.get('machine_id', 'unknown')
                timestamp = point.get('timestamp', datetime.utcnow().isoformat())
                
                # Validate input
                model_manager.validate_input_data(sensor_data)
                
                # Detect anomaly
                is_anomaly, metadata = model_manager.detect_anomaly(sensor_data)
                
                # Track per machine
                if machine_id not in machine_stats:
                    machine_stats[machine_id] = {
                        'total_points': 0,
                        'anomalies': 0,
                        'avg_score': 0,
                        'max_score': float('-inf'),
                        'min_score': float('inf')
                    }
                
                stats = machine_stats[machine_id]
                stats['total_points'] += 1
                if is_anomaly:
                    stats['anomalies'] += 1
                
                score = metadata['anomaly_score']
                stats['avg_score'] = (stats['avg_score'] * (stats['total_points'] - 1) + score) / stats['total_points']
                stats['max_score'] = max(stats['max_score'], score)
                stats['min_score'] = min(stats['min_score'], score)
                
                # Add to timeline
                anomaly_timeline.append({
                    'timestamp': timestamp,
                    'machine_id': machine_id,
                    'is_anomaly': is_anomaly,
                    'anomaly_score': score,
                    'severity': 'critical' if abs(score) > 2.0 else 
                               'high' if abs(score) > 1.0 else 
                               'medium' if abs(score) > 0.5 else 'low'
                })
                
            except Exception as e:
                logger.warning(f"Trend analysis failed for data point: {str(e)}")
                continue
        
        # Calculate anomaly rate per machine
        for machine_id, stats in machine_stats.items():
            stats['anomaly_rate'] = stats['anomalies'] / stats['total_points'] if stats['total_points'] > 0 else 0
        
        # Find machines with highest anomaly rates
        high_risk_machines = sorted(
            machine_stats.items(),
            key=lambda x: x[1]['anomaly_rate'],
            reverse=True
        )[:5]
        
        response = {
            'anomaly_timeline': anomaly_timeline,
            'machine_statistics': machine_stats,
            'high_risk_machines': [
                {
                    'machine_id': machine_id,
                    'anomaly_rate': stats['anomaly_rate'],
                    'total_anomalies': stats['anomalies'],
                    'avg_anomaly_score': stats['avg_score']
                }
                for machine_id, stats in high_risk_machines
            ],
            'summary': {
                'total_machines': len(machine_stats),
                'total_data_points': len(time_series_data),
                'total_anomalies': sum(stats['anomalies'] for stats in machine_stats.values()),
                'overall_anomaly_rate': sum(stats['anomalies'] for stats in machine_stats.values()) / len(time_series_data) if time_series_data else 0
            },
            'analysis_window_hours': window_size,
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'status': 'completed'
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Anomaly trend analysis failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@anomaly_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for anomaly detection service"""
    try:
        # Test anomaly detection with sample data
        test_data = np.random.normal(0, 1, 24)
        is_anomaly, metadata = model_manager.detect_anomaly(test_data)
        
        return jsonify({
            'service': 'Anomaly Detection API',
            'status': 'healthy',
            'model_available': 'anomaly_detector' in model_manager.models,
            'test_result': {
                'anomaly_detected': is_anomaly,
                'confidence': metadata.get('confidence', 0)
            },
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'service': 'Anomaly Detection API',
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500
