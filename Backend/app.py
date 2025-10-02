"""
Explainable Predictive Maintenance API
Main Flask application serving AI models and explanations
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import logging
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.prediction_api import prediction_bp
from api.explainability_api import explainability_bp
from api.anomaly_api import anomaly_bp
from api.data_api import data_bp
from utils.config import Config
from utils.logger import setup_logger

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for frontend communication
    CORS(app, origins=["http://localhost:8080", "http://localhost:3000"])
    
    # Setup logging
    setup_logger(app)
    
    # Register blueprints
    app.register_blueprint(prediction_bp, url_prefix='/api/v1/prediction')
    app.register_blueprint(explainability_bp, url_prefix='/api/v1/explainability')
    app.register_blueprint(anomaly_bp, url_prefix='/api/v1/anomaly')
    app.register_blueprint(data_bp, url_prefix='/api/v1/data')
    
    @app.route('/')
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'service': 'Predictive Maintenance API',
            'version': '2.1.0',
            'timestamp': datetime.now(datetime.timezone.utc).isoformat(),
            'endpoints': {
                'prediction': '/api/v1/prediction',
                'explainability': '/api/v1/explainability', 
                'anomaly': '/api/v1/anomaly',
                'data': '/api/v1/data'
            }
        })
    
    @app.route('/api/v1/status')
    def api_status():
        """API status with model information"""
        try:
            from AI.model_manager import ModelManager
            model_manager = ModelManager()
            models_status = model_manager.get_models_status()
            
            return jsonify({
                'status': 'operational',
                'models': models_status,
                'timestamp': datetime.now(datetime.timezone.utc).isoformat()
            })
        except Exception as e:
            app.logger.error(f"Status check failed: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now(datetime.timezone.utc).isoformat()
            }), 500
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
