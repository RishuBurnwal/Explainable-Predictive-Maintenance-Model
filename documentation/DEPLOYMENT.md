# Deployment Guide

This guide covers the steps to deploy the Explainable Predictive Maintenance Model in a production environment.

## Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (for production)
- Cloud provider account (AWS/Azure/GCP) or on-premises servers
- Domain name with SSL certificate (recommended)

## Deployment Options

### Option 1: Docker Compose (Recommended for small deployments)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/explainable-predictive-maintenance.git
   cd explainable-predictive-maintenance
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start the services:
   ```bash
   docker-compose up -d
   ```

### Option 2: Kubernetes (For production)

1. Set up your Kubernetes cluster
2. Install the required operators (e.g., cert-manager, ingress-nginx)
3. Deploy using Helm:
   ```bash
   helm install predictive-maintenance ./charts/predictive-maintenance \
     --set frontend.replicas=3 \
     --set backend.replicas=3
   ```

## Configuration

### Environment Variables

#### Frontend
```
VITE_API_URL=https://api.yourdomain.com
NODE_ENV=production
```

#### Backend
```
DATABASE_URL=postgresql://user:password@db:5432/predictive_maintenance
MODEL_PATH=/app/models/xgboost_model.pkl
FEATURE_STORE_URL=redis://redis:6379
```

## Scaling

### Horizontal Scaling
- Frontend: Scale by adding more instances behind a load balancer
- Backend: Scale API and model serving independently
- Database: Consider read replicas for high read throughput

### Vertical Scaling
- Increase CPU/memory for model serving
- Use GPUs for deep learning models if needed

## Monitoring

### Metrics Collection
- Prometheus for metrics collection
- Grafana for visualization
- Configure alerts for critical metrics

### Logging
- Centralized logging with ELK stack or similar
- Structured logging in JSON format
- Log rotation and retention policies

## Backup and Recovery

### Data Backup
- Regular database backups
- Model versioning with DVC
- Configuration backup

### Disaster Recovery
- Multi-region deployment for critical applications
- Regular recovery testing
- Documented recovery procedures

## Security

### Network Security
- Enable TLS/SSL for all endpoints
- Configure network policies
- Use private subnets for internal services

### Access Control
- Implement RBAC
- Regular access reviews
- Principle of least privilege

## Maintenance

### Updates
- Regular dependency updates
- Security patches
- Model retraining schedule

### Performance Tuning
- Database indexing
- Query optimization
- Caching strategies

## Troubleshooting

### Common Issues
1. **High Latency**
   - Check database queries
   - Review model inference time
   - Check network latency

2. **Memory Leaks**
   - Monitor memory usage
   - Check for unclosed resources
   - Review garbage collection settings

3. **Connection Issues**
   - Verify network connectivity
   - Check firewall rules
   - Review connection pooling settings
