# 🚀 Production Deployment Guide

## 📋 Overview

This guide covers deploying the Explainable Predictive Maintenance System to production environments.

## 🏗️ Build Process

### Frontend Build

```bash
# Development build
npm run build:dev

# Production build (optimized)
npm run build:prod

# Preview production build locally
npm run preview
```

### Backend Preparation

```bash
cd Backend

# Install production dependencies
pip install -r requirements.txt

# Set production environment
export FLASK_ENV=production
export FLASK_DEBUG=False

# Create optimized models
python setup.py
```

## 🌐 Deployment Options

### Option 1: Traditional Server Deployment

#### Frontend (Static Files)

**Using Nginx:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    root /var/www/predictmaint/dist;
    index index.html;
    
    # Handle client-side routing
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";
}
```

**Using Apache:**
```apache
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /var/www/predictmaint/dist
    
    # Handle client-side routing
    <Directory "/var/www/predictmaint/dist">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
        
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>
</VirtualHost>
```

#### Backend (Flask API)

**Using Gunicorn:**
```bash
# Install Gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# With configuration file
gunicorn -c gunicorn.conf.py app:app
```

**Gunicorn Configuration (`gunicorn.conf.py`):**
```python
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
```

### Option 2: Docker Deployment

#### Frontend Dockerfile

```dockerfile
# Build stage
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build:prod

# Production stage
FROM nginx:alpine

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Backend Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p models data logs temp

# Generate models and data
RUN python setup.py

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

#### Docker Compose

```yaml
version: '3.8'

services:
  frontend:
    build: 
      context: ./FrontEnd
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend
    environment:
      - VITE_API_BASE_URL=http://backend:5000/api/v1

  backend:
    build:
      context: ./Backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
    volumes:
      - ./Backend/models:/app/models
      - ./Backend/data:/app/data
      - ./Backend/logs:/app/logs
```

### Option 3: Cloud Deployment

#### AWS Deployment

**Frontend (S3 + CloudFront):**
```bash
# Build for production
npm run build:prod

# Deploy to S3
aws s3 sync dist/ s3://your-bucket-name --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

**Backend (ECS/Fargate):**
```json
{
  "family": "predictmaint-backend",
  "networkMode": "awsvpc",
  "requiresAttributes": [
    {
      "name": "com.amazonaws.ecs.capability.docker-remote-api.1.25"
    }
  ],
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "your-ecr-repo/predictmaint-backend:latest",
      "memory": 1024,
      "cpu": 512,
      "essential": true,
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ]
    }
  ]
}
```

#### Heroku Deployment

**Frontend:**
```bash
# Build and serve with serve
npm install -g serve
npm run build:prod
serve -s dist -l 3000
```

**Backend (`Procfile`):**
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

## 🔧 Environment Configuration

### Production Environment Variables

**Frontend (`.env.production`):**
```bash
VITE_API_BASE_URL=https://api.yourdomain.com/api/v1
VITE_APP_ENVIRONMENT=production
VITE_ENABLE_DEBUG_MODE=false
VITE_ENABLE_ANALYTICS=true
```

**Backend (`.env`):**
```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-super-secret-production-key
CORS_ORIGINS=https://yourdomain.com
LOG_LEVEL=INFO
```

## 🔒 Security Considerations

### SSL/TLS Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header Referrer-Policy "strict-origin-when-cross-origin";
}
```

### Backend Security

```python
# app.py production security
from flask_talisman import Talisman

app = create_app()

# Enable security headers
Talisman(app, force_https=True)

# Rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

## 📊 Monitoring & Logging

### Application Monitoring

```python
# Backend monitoring
import logging
from pythonjsonlogger import jsonlogger

# JSON logging for production
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

### Health Checks

```nginx
# Nginx health check endpoint
location /health {
    access_log off;
    return 200 "healthy\n";
    add_header Content-Type text/plain;
}
```

```python
# Backend health check
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

## 🚀 Performance Optimization

### Frontend Optimizations

```typescript
// Code splitting
const Documentation = lazy(() => import('./pages/Documentation'));

// Wrap in Suspense
<Suspense fallback={<LoadingSpinner />}>
  <Documentation />
</Suspense>
```

### Backend Optimizations

```python
# Redis caching
import redis
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@cache.memoize(timeout=300)
def expensive_prediction(sensor_data):
    return model.predict(sensor_data)
```

## 📋 Deployment Checklist

### Pre-deployment

- [ ] Run all tests (`npm test`, `python -m pytest`)
- [ ] Check linting (`npm run lint`, `flake8`)
- [ ] Build successfully (`npm run build:prod`)
- [ ] Verify environment variables
- [ ] Review security headers
- [ ] Test with production data

### Post-deployment

- [ ] Verify frontend loads correctly
- [ ] Test API endpoints
- [ ] Check SSL certificate
- [ ] Monitor application logs
- [ ] Verify error tracking
- [ ] Test error scenarios
- [ ] Performance testing

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run lint
      - run: npm run build:prod

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Your deployment commands here
          echo "Deploying to production..."
```

## 📞 Support & Maintenance

### Backup Strategy

- **Database:** Regular automated backups
- **Models:** Version-controlled model artifacts
- **Logs:** Centralized logging with retention policy
- **Configuration:** Infrastructure as code

### Monitoring Alerts

- API response time > 1000ms
- Error rate > 5%
- CPU usage > 80%
- Memory usage > 85%
- Disk space < 10%

---

🎉 **Your Explainable Predictive Maintenance system is now production-ready!**



