"""
Explainability API endpoints for SHAP and LIME explanations
"""

from flask import Blueprint, request, jsonify
import numpy as np
from datetime import datetime
import logging

from AI.model_manager import ModelManager
from AI.explainability import ModelExplainer

explainability_bp = Blueprint('explainability', __name__)
logger = logging.getLogger(__name__)

# Initialize model manager and explainer
model_manager = ModelManager()
explainer = ModelExplainer(model_manager)

@explainability_bp.route('/shap', methods=['POST'])
def get_shap_explanation():
    """
    Get SHAP explanation for a prediction
    
    Expected input:
    {
        "sensor_data": [24 sensor values],
        "model_type": "rul" or "failure",
        "machine_id": "optional machine identifier",
        "max_features": 10
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'sensor_data' not in data:
            return jsonify({'error': 'Missing sensor_data in request'}), 400
        
        sensor_data = np.array(data['sensor_data'])
        model_type = data.get('model_type', 'rul')
        machine_id = data.get('machine_id', 'unknown')
        max_features = data.get('max_features', 10)
        
        # Validate input
        model_manager.validate_input_data(sensor_data)
        
        if model_type not in ['rul', 'failure']:
            return jsonify({'error': 'model_type must be "rul" or "failure"'}), 400
        
        # Get SHAP explanation
        shap_explanation = explainer.get_shap_explanation(
            model_type, sensor_data, max_features
        )
        
        # Add metadata
        shap_explanation.update({
            'machine_id': machine_id,
            'request_timestamp': datetime.utcnow().isoformat(),
            'status': 'success'
        })
        
        return jsonify(shap_explanation)
        
    except ValueError as e:
        logger.warning(f"Validation error in SHAP explanation: {str(e)}")
        return jsonify({'error': str(e), 'status': 'validation_error'}), 400
        
    except Exception as e:
        logger.error(f"SHAP explanation failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@explainability_bp.route('/lime', methods=['POST'])
def get_lime_explanation():
    """
    Get LIME explanation for a prediction
    
    Expected input:
    {
        "sensor_data": [24 sensor values],
        "model_type": "rul" or "failure",
        "machine_id": "optional machine identifier",
        "num_features": 10
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'sensor_data' not in data:
            return jsonify({'error': 'Missing sensor_data in request'}), 400
        
        sensor_data = np.array(data['sensor_data'])
        model_type = data.get('model_type', 'failure')
        machine_id = data.get('machine_id', 'unknown')
        num_features = data.get('num_features', 10)
        
        # Validate input
        model_manager.validate_input_data(sensor_data)
        
        if model_type not in ['rul', 'failure']:
            return jsonify({'error': 'model_type must be "rul" or "failure"'}), 400
        
        # Get LIME explanation
        lime_explanation = explainer.get_lime_explanation(
            sensor_data, model_type, num_features
        )
        
        # Add metadata
        lime_explanation.update({
            'machine_id': machine_id,
            'request_timestamp': datetime.utcnow().isoformat(),
            'status': 'success'
        })
        
        return jsonify(lime_explanation)
        
    except ValueError as e:
        logger.warning(f"Validation error in LIME explanation: {str(e)}")
        return jsonify({'error': str(e), 'status': 'validation_error'}), 400
        
    except Exception as e:
        logger.error(f"LIME explanation failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@explainability_bp.route('/comprehensive', methods=['POST'])
def get_comprehensive_explanation():
    """
    Get comprehensive explanation combining SHAP and LIME
    
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
        
        # Get comprehensive analysis
        comprehensive_analysis = explainer.get_feature_impact_analysis(sensor_data)
        
        # Add metadata
        comprehensive_analysis.update({
            'machine_id': machine_id,
            'request_timestamp': datetime.utcnow().isoformat(),
            'status': 'success'
        })
        
        return jsonify(comprehensive_analysis)
        
    except ValueError as e:
        logger.warning(f"Validation error in comprehensive explanation: {str(e)}")
        return jsonify({'error': str(e), 'status': 'validation_error'}), 400
        
    except Exception as e:
        logger.error(f"Comprehensive explanation failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@explainability_bp.route('/feature-importance', methods=['POST'])
def get_feature_importance():
    """
    Get global feature importance for a model
    
    Expected input:
    {
        "model_type": "rul" or "failure",
        "top_n": 15
    }
    """
    try:
        data = request.get_json()
        model_type = data.get('model_type', 'rul') if data else 'rul'
        top_n = data.get('top_n', 15) if data else 15
        
        if model_type not in ['rul', 'failure']:
            return jsonify({'error': 'model_type must be "rul" or "failure"'}), 400
        
        # Generate sample data for global importance
        from AI.pretrained_models import generate_synthetic_turbofan_data
        sample_data, _, _ = generate_synthetic_turbofan_data(100)
        
        # Get feature importance for multiple samples
        importance_scores = {}
        feature_names = explainer.feature_names
        
        for _, row in sample_data.head(20).iterrows():  # Use 20 samples
            shap_exp = explainer.get_shap_explanation(model_type, row.values)
            
            if 'feature_importance' in shap_exp:
                for feature_info in shap_exp['feature_importance']:
                    feature = feature_info['feature']
                    if feature not in importance_scores:
                        importance_scores[feature] = []
                    importance_scores[feature].append(feature_info['abs_importance'])
        
        # Calculate average importance
        global_importance = []
        for feature, scores in importance_scores.items():
            avg_importance = np.mean(scores)
            global_importance.append({
                'feature': feature,
                'importance': float(avg_importance),
                'std_dev': float(np.std(scores)),
                'samples': len(scores)
            })
        
        # Sort by importance
        global_importance.sort(key=lambda x: x['importance'], reverse=True)
        
        response = {
            'model_type': model_type,
            'global_feature_importance': global_importance[:top_n],
            'total_features': len(feature_names),
            'analysis_samples': len(sample_data),
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'success'
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Feature importance analysis failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@explainability_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for explainability service"""
    try:
        # Test if explainers are working
        test_data = np.random.normal(0, 1, 24)
        shap_test = explainer.get_shap_explanation('rul', test_data, max_display=3)
        
        explainer_status = {
            'shap_available': 'error' not in shap_test,
            'lime_available': 'tabular' in explainer.lime_explainers,
            'feature_count': len(explainer.feature_names)
        }
        
        return jsonify({
            'service': 'Explainability API',
            'status': 'healthy',
            'explainers': explainer_status,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'service': 'Explainability API',
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500
