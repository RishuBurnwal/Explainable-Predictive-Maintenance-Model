"""
Logging configuration for the Predictive Maintenance API
"""

import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(app):
    """Setup application logging"""
    
    if not app.debug and not app.testing:
        # Production logging
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/predictive_maintenance.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Predictive Maintenance API startup')
    
    else:
        # Development logging
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        app.logger.addHandler(console_handler)
        app.logger.setLevel(logging.DEBUG)
