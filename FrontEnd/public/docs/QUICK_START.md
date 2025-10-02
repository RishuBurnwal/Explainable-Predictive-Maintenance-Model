# 🚀 Quick Start Guide

## ⚡ Super Fast Setup (Recommended)

### Using the Universal Setup Manager
```bash
# Run the unified setup script
python setup_manager.py

# Choose your platform and select:
# 3. 🚀 Run Both Frontend & Backend
```

This will automatically:
- Start backend server (http://localhost:5000)
- Start frontend server (http://localhost:5173)
- Optionally open both in your browser

---

## 📋 Manual Setup (Alternative)

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Windows PowerShell** or equivalent terminal

### 1. Start Backend Server

```bash
# Navigate to backend directory
cd "Backend"

# Install Python dependencies (first time only)
pip install -r requirements.txt

# Start the Flask server
python app.py
```

**Backend will be available at: http://localhost:5000**

#### Backend Health Check
```bash
curl http://localhost:5000/api/v1/status
```

### 2. Start Frontend Server

```bash
# Navigate to frontend directory (in a new terminal)
cd "FrontEnd"

# Install Node dependencies (first time only)
npm install

# Start the development server
npm run dev
```

**Frontend will be available at: http://localhost:5173**

### 3. Verify Connection

1. Open your browser to **http://localhost:5173**
2. Check that the dashboard shows **"Connected"** status
3. Verify real-time data is updating (not demo data)
4. Test navigation between sections

## 🎯 Quick Tips

### Using Setup Manager Benefits:
- **⚡ Faster Setup**: One command starts everything
- **🔧 Auto-Configuration**: Handles virtual environments
- **🖥️ Cross-Platform**: Works on Windows, Linux, and macOS
- **🌐 Browser Integration**: Optional auto-open functionality
- **✅ Health Checks**: Built-in validation and testing

### Development Workflow:
1. Run `python setup_manager.py`
2. Select "🚀 Run Both Frontend & Backend"
3. Choose 'y' to open both services in browser
4. Start coding with live reload!

## Common Issues

### Backend Not Starting
```bash
# Check if Python is installed
python --version

# Install missing dependencies
pip install flask flask-cors pandas numpy scikit-learn xgboost lightgbm

# Make sure you're in the Backend directory
cd "C:\Users\rishu\OneDrive\Desktop\Explainable Predictive Maintenance Model\Backend"
```

### Frontend Not Starting
```bash
# Check if Node.js is installed
node --version
npm --version

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Make sure you're in the FrontEnd directory
cd "C:\Users\rishu\OneDrive\Desktop\Explainable Predictive Maintenance Model\FrontEnd"
```

### Connection Failed
1. Ensure both servers are running
2. Check no other applications are using ports 5000 or 8080
3. Verify firewall is not blocking the connections
4. Check browser console for error messages

## Development Commands

### Backend
```bash
# Run tests
python test_api.py

# Start with debug mode
python app.py --debug

# Check installed packages
pip list
```

### Frontend
```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Run type checking
npm run typecheck

# Fix linting issues
npm run lint:fix
```

## Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed production setup instructions.

## Next Steps

1. **Explore the Dashboard**: Navigate through different sections
2. **Check Documentation**: Visit the Documentation page for detailed guides
3. **Monitor Real-time Data**: Watch the live charts and status updates
4. **Test Predictions**: Upload sensor data or use generated samples
5. **Review Explanations**: Check SHAP and LIME model explanations

## Support

If you encounter issues:
1. Check the [FAQ](./FAQ.md) for common solutions
2. Review browser console for JavaScript errors
3. Check backend logs for Python errors
4. Ensure all dependencies are correctly installed

**Happy monitoring! 🎯**



