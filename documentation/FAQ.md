# Frequently Asked Questions

## General

### What is the purpose of this project?
This project aims to provide a predictive maintenance solution that not only predicts equipment failures but also explains the predictions using explainable AI techniques. It now includes a complete IoT sensor network with real-time monitoring capabilities.

### What types of equipment is this system designed for?
The system is designed to be adaptable to various types of industrial equipment, particularly those with sensor data that can indicate potential failures. It includes 16 industrial sensors across 4 production lines:
- Turbofan Engines (6 sensors)
- Hydraulic Systems (3 sensors)
- Electric Motors (3 sensors)
- Quality Control & Cooling (4 sensors)

### Who developed this project?
This project was developed by Rishu Burnwal, a Full Stack AI/ML Engineer & Software Developer specializing in machine learning, full-stack development, and cloud computing.

## Technical

### What machine learning algorithms are used?
The system uses multiple machine learning algorithms:
- **XGBoost**: For Remaining Useful Life (RUL) prediction
- **LightGBM**: For failure risk classification
- **Isolation Forest**: For anomaly detection
- **SHAP & LIME**: For model explainability and interpretability

### How accurate are the predictions?
Model accuracy depends on the quality and quantity of training data:
- **RUL Prediction**: 95%+ accuracy on test sets
- **Failure Risk Classification**: 92%+ accuracy
- **Anomaly Detection**: <5% false positive rate
These metrics are based on the NASA C-MAPSS turbofan engine degradation dataset.

### How often is the model retrained?
The system uses pre-trained models that were trained on the NASA C-MAPSS dataset. For production use:
- Models should be retrained weekly or monthly
- Retrain after significant data drift is detected
- Retrain when new labeled failure data becomes available
- Continuous learning pipelines can be implemented for automatic retraining

### How does the IoT sensor integration work?
The system includes a simulation of 16 industrial sensors across 4 production lines:
- **Turbofan Engines** (6 sensors): Core Temperature, Fan Vibration, Compressor Pressure, Turbine RPM, Exhaust Temperature, Bearing Vibration
- **Hydraulic Systems** (3 sensors): Pump Temperature, System Pressure, Flow Rate
- **Electric Motors** (3 sensors): Current, Voltage, Torque
- **Quality Control & Cooling** (4 sensors): Spindle Temperature, Spindle Vibration, Coolant Temperature, Coolant Flow

Sensors update every 2 seconds and can be toggled on/off through the web interface. Each sensor has adjustable age/degradation settings (0-100%).

### What programming languages and frameworks are used?
- **Frontend**: React 18 + TypeScript, Vite, TailwindCSS, Shadcn/ui
- **Backend**: Python 3.8+, Flask, NumPy, Pandas, Scikit-learn
- **ML Libraries**: XGBoost, LightGBM, SHAP, LIME
- **Data Visualization**: Recharts
- **Deployment**: Cross-platform compatible (Windows, Linux, macOS)

## Troubleshooting

### The frontend isn't connecting to the backend
1. Ensure the backend server is running (`python app.py` in Backend directory)
2. Check that the API URL in the frontend is correct (http://localhost:5000)
3. Verify CORS settings in the backend (should allow localhost:8080)
4. Check the browser's developer console for errors
5. Verify network connectivity between frontend and backend

### Model predictions seem inaccurate
1. Check the data quality of recent inputs
2. Verify that all required features are being provided (24 features expected)
3. Check if the sensors providing data are active and in normal status
4. Review the model's confidence scores in the dashboard
5. Consider retraining with more recent data if deployed in production

### IoT sensors are not updating
1. Verify the backend sensor manager is running (starts automatically with app.py)
2. Check the sensor update interval configuration (default: 2 seconds)
3. Review backend logs for sensor processing errors
4. Ensure no exceptions are occurring in the sensor manager
5. Check if sensors are set to inactive status (toggle to reactivate)

### The setup manager is not working
1. Ensure Python 3.8+ is installed and accessible
2. Check Node.js 16+ is installed
3. Verify Git is installed (recommended but optional)
4. Run `python setup_manager.py` from the project root
5. Check console output for specific error messages

### Backend dependencies are not installing
1. Ensure you're in the Backend directory
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Check for network connectivity issues or corporate firewalls

### Frontend dependencies are not installing
1. Ensure Node.js 16+ is installed
2. Check npm is accessible from command line
3. Run `npm install` from the FrontEnd directory
4. Clear npm cache if needed: `npm cache clean --force`
5. Delete node_modules and package-lock.json, then reinstall

## Deployment

### What are the system requirements?
- **Minimum**: 4GB RAM, 2 CPU cores, 5GB free disk space
- **Recommended**: 8GB+ RAM, 4+ CPU cores, 10GB+ free disk space
- **Development**: Same as recommended
- **Production**: 16GB+ RAM, 8+ CPU cores, 20GB+ free disk space

### How do I deploy this in production?
1. **Backend**: Use Gunicorn or similar WSGI server instead of Flask development server
2. **Frontend**: Build static files with `npm run build` and serve with nginx/Apache
3. **Reverse Proxy**: Configure nginx to serve frontend and proxy API requests to backend
4. **SSL**: Enable HTTPS with Let's Encrypt or similar certificate authority
5. **Process Management**: Use systemd, supervisor, or similar for service management

### How do I scale the system for more users?
1. Add more backend API server instances behind a load balancer
2. Use multiple frontend servers or CDN for static assets
3. Implement caching for frequently accessed data (Redis/Memcached)
4. Scale IoT data processing by adjusting sensor update intervals
5. Consider database optimization if external storage is added

### How do I monitor the system in production?
1. **Backend**: Monitor logs through configured logging system
2. **Frontend**: Use browser performance tools and error tracking
3. **IoT Sensors**: Monitor sensor network health through dashboard
4. **API Health**: Use built-in health check endpoints (`/` and `/api/v1/status`)
5. **System Resources**: Monitor CPU, memory, and disk usage

## Customization

### How do I add more sensors to the network?
1. Edit `Backend/AI/sensor_manager.py`
2. Add new sensor entries to the `factory_sensors` list
3. Define sensor properties (name, type, location, description)
4. Restart the backend server
5. The new sensors will appear in the frontend dashboard

### How do I customize the ML models?
1. **Retraining**: Use notebooks in `models/notebooks/` for model development
2. **New Models**: Add model loading functions in `Backend/AI/model_manager.py`
3. **API Integration**: Add new endpoints in appropriate API files in `Backend/api/`
4. **Frontend Integration**: Update frontend components to display new model results
5. **Testing**: Update `Backend/test_api.py` with tests for new functionality

### How do I modify the frontend dashboard?
1. **Components**: Modify files in `FrontEnd/src/components/`
2. **Pages**: Modify files in `FrontEnd/src/pages/`
3. **Styles**: Update TailwindCSS classes or add custom CSS in `FrontEnd/src/App.css`
4. **API Calls**: Update `FrontEnd/src/lib/api.ts` for new endpoints
5. **Build**: Run `npm run dev` for development or `npm run build` for production

## Support

### Where can I get help with implementation?
- Check the project's GitHub repository for issues and discussions
- Review the comprehensive documentation in the `documentation/` folder
- Contact the developer through GitHub or email (rishu.burnwal@gmail.com)
- Refer to the detailed setup guides and architecture documentation

### How can I contribute to the project?
1. Fork the repository on GitHub
2. Create a feature branch for your changes
3. Make your improvements or bug fixes
4. Write tests if applicable
5. Submit a pull request with a clear description of your changes
6. Follow the existing code style and documentation practices

### How do I report bugs or request features?
1. Open an issue on the GitHub repository
2. Provide detailed information about the problem or request
3. Include steps to reproduce for bug reports
4. Specify your environment (OS, Python version, Node.js version)
5. Attach screenshots or logs if relevant

### Is commercial use allowed?
Yes, this project is licensed under the MIT License, which allows for commercial use, modification, distribution, and patent use. See the LICENSE file for complete details.