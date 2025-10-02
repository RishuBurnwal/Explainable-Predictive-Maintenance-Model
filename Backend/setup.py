"""
Setup script for Explainable Predictive Maintenance Backend
Initializes models, creates sample data, and prepares the environment
"""

import os
import sys
import subprocess
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def install_requirements():
    """Install required Python packages"""
    logger.info("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        'models',
        'data/sample_datasets',
        'logs',
        'temp'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"✅ Created directory: {directory}")

def generate_sample_data():
    """Generate sample datasets"""
    logger.info("Generating sample datasets...")
    try:
        from data.sample_turbofan_data import save_sample_datasets
        save_sample_datasets()
        logger.info("✅ Sample datasets generated successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to generate sample data: {e}")
        return False

def create_pretrained_models():
    """Create and save pretrained models"""
    logger.info("Creating pretrained models...")
    try:
        from AI.pretrained_models import save_models_to_disk
        save_models_to_disk('models')
        logger.info("✅ Pretrained models created and saved")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create models: {e}")
        return False

def test_model_loading():
    """Test if models can be loaded successfully"""
    logger.info("Testing model loading...")
    try:
        from AI.model_manager import ModelManager
        model_manager = ModelManager()
        
        # Test predictions
        import numpy as np
        test_data = np.random.normal(0, 1, 24)
        
        rul_pred, rul_meta = model_manager.predict_rul(test_data)
        risk_pred, risk_meta = model_manager.predict_failure_risk(test_data)
        anomaly_pred, anomaly_meta = model_manager.detect_anomaly(test_data)
        
        logger.info(f"✅ Model testing successful:")
        logger.info(f"   RUL Prediction: {rul_pred:.2f} hours")
        logger.info(f"   Risk Level: {risk_pred}")
        logger.info(f"   Anomaly Detected: {anomaly_pred}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Model testing failed: {e}")
        return False

def create_env_file():
    """Create environment configuration file"""
    env_content = f"""# Explainable Predictive Maintenance Backend Configuration
# Generated on {datetime.now().isoformat()}

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-in-production

# API Configuration
API_VERSION=v1
MAX_CONTENT_LENGTH=16777216

# Model Configuration
MODEL_DIR=models
DATA_DIR=data
LOG_LEVEL=INFO

# CORS Configuration
CORS_ORIGINS=http://localhost:8080,http://localhost:3000

# Database Configuration (if needed in future)
# DATABASE_URL=sqlite:///predictive_maintenance.db
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    logger.info("✅ Environment file created (.env)")

def create_startup_script():
    """Create startup script for easy server launch"""
    
    # Windows batch script
    windows_script = """@echo off
echo Starting Explainable Predictive Maintenance Backend...
echo.

REM Activate virtual environment if it exists
if exist venv\\Scripts\\activate.bat (
    echo Activating virtual environment...
    call venv\\Scripts\\activate.bat
)

REM Start the Flask application
echo Starting Flask server on http://localhost:5000
python app.py

pause
"""
    
    with open('start_server.bat', 'w') as f:
        f.write(windows_script)
    
    # Unix shell script
    unix_script = """#!/bin/bash
echo "Starting Explainable Predictive Maintenance Backend..."
echo

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Start the Flask application
echo "Starting Flask server on http://localhost:5000"
python app.py
"""
    
    with open('start_server.sh', 'w') as f:
        f.write(unix_script)
    
    # Make shell script executable
    try:
        os.chmod('start_server.sh', 0o755)
    except:
        pass  # Windows doesn't support chmod
    
    logger.info("✅ Startup scripts created (start_server.bat, start_server.sh)")

def main():
    """Main setup function"""
    logger.info("🚀 Setting up Explainable Predictive Maintenance Backend...")
    logger.info("=" * 60)
    
    success_count = 0
    total_steps = 6
    
    # Step 1: Create directories
    create_directories()
    success_count += 1
    
    # Step 2: Install requirements
    if install_requirements():
        success_count += 1
    
    # Step 3: Create environment file
    create_env_file()
    success_count += 1
    
    # Step 4: Generate sample data
    if generate_sample_data():
        success_count += 1
    
    # Step 5: Create pretrained models
    if create_pretrained_models():
        success_count += 1
    
    # Step 6: Test model loading
    if test_model_loading():
        success_count += 1
    
    # Create startup scripts
    create_startup_script()
    
    # Final summary
    logger.info("=" * 60)
    logger.info(f"Setup completed: {success_count}/{total_steps} steps successful")
    
    if success_count == total_steps:
        logger.info("🎉 Backend setup completed successfully!")
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Run 'python app.py' to start the server")
        logger.info("2. Or use the startup scripts:")
        logger.info("   - Windows: start_server.bat")
        logger.info("   - Unix/Mac: ./start_server.sh")
        logger.info("3. API will be available at http://localhost:5000")
        logger.info("4. Check API status at http://localhost:5000/api/v1/status")
    else:
        logger.warning("⚠️  Setup completed with some issues. Check the logs above.")
        logger.info("You may need to manually install dependencies or fix configuration.")

if __name__ == "__main__":
    main()
