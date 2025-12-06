# Deployment Guide

This guide covers the steps to deploy the Explainable Predictive Maintenance Model in a production environment.

## Prerequisites

- Python 3.8+
- Node.js 16+
- Git
- Linux/Unix server or Windows Server
- Reverse proxy server (nginx, Apache) for production deployment
- SSL certificate (recommended)

## Deployment Options

### Option 1: Direct Deployment (Recommended for production)

1. Clone the repository:
   ```bash
   git clone https://github.com/RishuBurnwal/Explainable-Predictive-Maintenance-Model.git
   cd Explainable-Predictive-Maintenance-Model
   ```

2. Install backend dependencies:
   ```bash
   cd Backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd ../FrontEnd
   npm install
   ```

4. Build the frontend for production:
   ```bash
   npm run build
   ```

### Option 2: Using Universal Setup Manager

1. Clone the repository:
   ```bash
   git clone https://github.com/RishuBurnwal/Explainable-Predictive-Maintenance-Model.git
   cd Explainable-Predictive-Maintenance-Model
   ```

2. Run the setup manager:
   ```bash
   python setup_manager.py
   ```

3. Select "Complete Setup (Install Dependencies)" to install all required packages

## Production Deployment

### Backend Deployment

For production deployment, use a WSGI server like Gunicorn instead of the Flask development server:

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Run the backend with Gunicorn:
   ```bash
   cd Backend
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

Configuration options:
- `-w 4`: Number of worker processes
- `-b 0.0.0.0:5000`: Bind to all interfaces on port 5000

### Frontend Deployment

The frontend build creates static files that can be served by any web server:

1. Build the frontend:
   ```bash
   cd FrontEnd
   npm run build
   ```

2. The built files will be in the `dist` directory and can be served by:
   - nginx
   - Apache
   - Caddy
   - Any static file server

Example nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /path/to/FrontEnd/dist;
        try_files $uri $uri/ /index.html;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /api/ {
        proxy_pass http://localhost:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Configuration

### Environment Variables

#### Backend Configuration
The backend configuration is managed through `Backend/utils/config.py`:
- PORT: Backend port (default: 5000)
- SENSOR_UPDATE_INTERVAL: IoT sensor update frequency in seconds (default: 2)
- DEBUG: Debug mode (default: False in production)

#### Frontend Configuration
The frontend configuration is in `FrontEnd/vite.config.ts`:
- API base URL: http://localhost:5000 (should be updated for production)
- Build output directory: dist/

## Scaling

### Horizontal Scaling

#### Frontend
- Serve static files from CDN
- Use multiple frontend servers behind a load balancer
- Enable gzip compression

#### Backend
- Run multiple backend instances behind a load balancer
- Use Redis or similar for session storage if needed
- Scale IoT sensor processing workers

### Vertical Scaling
- Increase CPU/memory for model serving
- Optimize database queries if external database is used
- Use caching for frequently accessed data

## Monitoring

### Backend Monitoring
- Built-in logging through `Backend/utils/logger.py`
- Health check endpoint at `/`
- API status endpoint at `/api/v1/status`

### Frontend Monitoring
- Console logging for debugging
- Error boundaries for React component errors
- Performance monitoring through browser dev tools

### IoT Sensor Network Monitoring
- Real-time sensor health status
- Network statistics dashboard
- Critical/warning sensor alerts

## Backup and Recovery

### Model Backup
- ML models are stored in `Backend/models/`
- Version control through Git
- Regular backups of trained model files

### Configuration Backup
- Application configuration in `Backend/utils/config.py`
- Frontend configuration in `FrontEnd/vite.config.ts`
- Version control through Git

### Data Considerations
- The system currently uses in-memory storage for sensor data
- For production use, consider persistent storage solutions
- IoT sensor data can be archived to external databases

## Security

### Network Security
- Use HTTPS in production
- Configure CORS properly (currently allows localhost:8080)
- Use firewalls to restrict access to backend ports

### Application Security
- Input validation for all API endpoints
- Error handling to prevent information leakage
- Secure headers in production deployment

### IoT Sensor Security
- Sensor network simulation (no external connections in current implementation)
- Data validation for sensor readings
- Access controls through frontend interface

## Maintenance

### Updates
- Regular dependency updates through package managers
- Security patches for underlying system
- Model retraining and updates as needed
- Git-based deployment for easy rollbacks

### Performance Tuning
- Optimize ML model inference
- Efficient data processing in sensor manager
- Caching strategies for repeated calculations
- Database optimization if external storage is added

## Troubleshooting

### Common Issues

1. **Backend Not Starting**
   - Check Python virtual environment activation
   - Verify all dependencies are installed
   - Check port availability
   - Review error logs in console output

2. **Frontend Not Building**
   - Verify Node.js version (16+)
   - Check npm dependencies installation
   - Review build errors in console output

3. **API Connection Issues**
   - Verify backend is running
   - Check CORS configuration
   - Review network connectivity between frontend and backend
   - Confirm API base URL configuration

4. **IoT Sensor Problems**
   - Check sensor manager initialization
   - Review sensor data processing logs
   - Verify sensor activation status through API
   - Confirm real-time updates are functioning

5. **Performance Issues**
   - Monitor system resource usage
   - Check ML model inference times
   - Review sensor data processing efficiency
   - Optimize frontend rendering performance

### Logs and Diagnostics

#### Backend Logs
- Console output from Flask application
- Structured logging through Python logging module
- Error traces for debugging

#### Frontend Logs
- Browser console for JavaScript errors
- Network tab for API request/response analysis
- React DevTools for component performance

#### Health Checks
- Backend health: `GET http://localhost:5000/`
- API status: `GET http://localhost:5000/api/v1/status`
- Sensor network health: `GET http://localhost:5000/api/v1/sensors/health`