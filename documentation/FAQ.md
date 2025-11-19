# Frequently Asked Questions

## General

### What is the purpose of this project?
This project aims to provide a predictive maintenance solution that not only predicts equipment failures but also explains the predictions using explainable AI techniques. It now includes a complete IoT sensor network with real-time monitoring capabilities.

### What types of equipment is this system designed for?
The system is designed to be adaptable to various types of industrial equipment, particularly those with sensor data that can indicate potential failures. It includes 16 industrial sensors across 4 production lines.

## Technical

### What machine learning algorithms are used?
The system primarily uses XGBoost for predictive modeling, with SHAP values for explainability. Other algorithms can be integrated as needed, including LightGBM for classification and Isolation Forest for anomaly detection.

### How accurate are the predictions?
Model accuracy depends on the quality and quantity of training data. Typical models achieve 85-95% accuracy on test sets, but this varies by use case.

### How often is the model retrained?
The retraining frequency is configurable. A common approach is to retrain:
- Weekly for models in production
- After significant data drift is detected
- When new labeled failure data becomes available

### How does the IoT sensor integration work?
The system includes a simulation of 16 industrial sensors across 4 production lines:
- Turbofan Engines (6 sensors)
- Hydraulic Systems (3 sensors)
- Electric Motors (3 sensors)
- Quality Control & Cooling (4 sensors)

Sensors update every 2 seconds and can be toggled on/off through the web interface.

## Troubleshooting

### The frontend isn't connecting to the backend
1. Ensure the backend server is running
2. Check that the API URL in the frontend configuration is correct
3. Verify CORS settings in the backend
4. Check the browser's developer console for errors

### Model predictions seem inaccurate
1. Check the data quality of recent inputs
2. Verify that all required features are being provided
3. Check if the model needs retraining
4. Review the model's confidence scores

### IoT sensors are not updating
1. Verify the backend sensor manager is running
2. Check the sensor update interval configuration
3. Review backend logs for sensor processing errors
4. Ensure no network issues are affecting sensor data

## Deployment

### What are the system requirements?
- **Development**: 8GB RAM, 4 CPU cores, 10GB free disk space
- **Production**: 16GB+ RAM, 8+ CPU cores, 50GB+ free disk space

### How do I scale the system for more users?
1. Add more API server instances behind a load balancer
2. Use a managed database service
3. Implement caching for frequently accessed data
4. Scale IoT data processing workers for more sensors

## Support

### Where can I get help with implementation?
- Check the project's GitHub issues
- Review the documentation
- Contact the maintainers through the project's GitHub repository

### How can I contribute to the project?
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request with a clear description of your changes