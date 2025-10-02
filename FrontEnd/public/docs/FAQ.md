# ❓ Frequently Asked Questions (FAQ)

## 🚀 Getting Started

### Q: What is this project about?
**A:** This is an **Explainable Predictive Maintenance System** that uses AI to predict equipment failures and provides transparent explanations for its predictions using SHAP and LIME techniques.

### Q: What technologies are used?
**A:** 
- **Frontend:** React, TypeScript, Tailwind CSS, Vite
- **Backend:** Flask, Python, scikit-learn
- **AI Models:** XGBoost, LightGBM, Isolation Forest
- **Explainability:** SHAP, LIME
- **Data:** NASA Turbofan-inspired synthetic datasets

### Q: Do I need real sensor data to use this?
**A:** No! The system comes with **synthetic NASA Turbofan datasets** that simulate realistic engine sensor data. You can also connect your own sensor data via the API.

## 🛠️ Installation & Setup

### Q: I'm getting "Module not found" errors. What should I do?
**A:** 
1. Make sure you're in the correct directory (`Backend/` or `FrontEnd/`)
2. Install dependencies:
   ```bash
   # For Backend
   cd Backend && pip install -r requirements.txt
   
   # For Frontend  
   cd FrontEnd && npm install
   ```

### Q: The setup script fails. What are the alternatives?
**A:** If `python setup.py` fails, try manual setup:
```bash
cd Backend
pip install -r requirements.txt
mkdir models data/sample_datasets logs temp
python data/sample_turbofan_data.py
python AI/pretrained_models.py
python app.py
```

### Q: Which Python version should I use?
**A:** Python 3.8 or higher is required. Python 3.9-3.11 are recommended for best compatibility.

### Q: The frontend won't start. What's wrong?
**A:** Common solutions:
1. Make sure Node.js 16+ is installed
2. Clear cache: `npm cache clean --force`
3. Delete `node_modules` and run `npm install` again
4. Check if port 8080 is available

## 🔗 Connectivity Issues

### Q: Frontend shows "Backend connection failed". How to fix?
**A:** 
1. **Check backend is running:** Visit `http://localhost:5000/api/v1/status`
2. **Check CORS settings:** Ensure backend allows frontend origin
3. **Verify ports:** Backend on 5000, Frontend on 8080
4. **Check firewall:** Make sure ports aren't blocked

### Q: I see "Demo Mode" everywhere. Is this normal?
**A:** Yes! When the backend isn't connected, the frontend automatically switches to demo mode with mock data. Start the backend to see real predictions.

### Q: API requests are slow. How can I speed them up?
**A:** 
- **Model loading:** Models load once at startup (~2-3 seconds)
- **Prediction time:** Should be <100ms per request
- **Batch requests:** Use batch endpoints for multiple predictions
- **Caching:** Enable Redis for frequently accessed data

## 🧠 AI Models & Data

### Q: How accurate are the AI models?
**A:** 
- **RUL Predictor (XGBoost):** R² > 0.85
- **Failure Classifier (LightGBM):** Accuracy > 0.90
- **Anomaly Detector (Isolation Forest):** Precision > 0.80

### Q: What do the sensor features represent?
**A:** The 24 features include:
- **3 Operational Settings:** Altitude, Mach number, Throttle angle
- **21 Sensors:** Temperature (7), Pressure (5), Speed (3), Flow (6)

### Q: Can I use my own datasets?
**A:** Yes! You can:
1. **Upload via API:** Use `/api/v1/data/upload` endpoint
2. **Replace sample data:** Put your CSV files in `Backend/data/sample_datasets/`
3. **Custom format:** Ensure 24 features match the expected sensor layout

### Q: What is SHAP and LIME?
**A:** 
- **SHAP (SHapley Additive exPlanations):** Shows how each feature contributes to predictions
- **LIME (Local Interpretable Model-agnostic Explanations):** Explains individual predictions by perturbing input features
- Both help make AI decisions transparent and trustworthy

## 🎛️ Dashboard & Features

### Q: The "Start Live Feed" button doesn't work. Why?
**A:** 
- **Backend must be running** on port 5000
- Check network connection between frontend and backend
- Look for error messages in browser console (F12)
- Verify API endpoints are responding

### Q: Charts show no data or errors. What's happening?
**A:** 
1. **Check connection status** indicator in the dashboard
2. **Refresh data** using the refresh button
3. **Check browser console** for JavaScript errors
4. **Verify API responses** at `http://localhost:5000/api/v1/status`

### Q: How often does real-time data update?
**A:** 
- **Live feed:** Every 5 seconds when enabled
- **Status cards:** Every 30 seconds  
- **Manual refresh:** Available via refresh buttons

### Q: Can I change the update intervals?
**A:** Yes! Edit the intervals in the frontend components:
- `DataVisualization.tsx`: Live feed interval
- `Index.tsx`: Status card refresh interval

## 📊 Predictions & Results

### Q: What does RUL mean?
**A:** **RUL (Remaining Useful Life)** is the predicted time until the equipment needs maintenance, typically measured in hours or cycles.

### Q: How should I interpret risk levels?
**A:** 
- **Low Risk (Green):** Normal operation, no immediate action needed
- **Medium Risk (Yellow):** Monitor closely, plan maintenance
- **High Risk (Red):** Immediate attention required, schedule maintenance soon

### Q: Are anomaly scores reliable?
**A:** Anomaly scores range from 0-1:
- **0.0-0.3:** Normal operation
- **0.3-0.7:** Potential anomaly, investigate
- **0.7-1.0:** High probability anomaly, take action

### Q: Can I adjust prediction thresholds?
**A:** Yes! Modify thresholds in `Backend/utils/config.py`:
```python
THRESHOLDS = {
    'anomaly_threshold': 0.5,
    'high_risk_threshold': 0.7,
    'low_rul_threshold': 50
}
```

## 🔧 Customization

### Q: How do I add new AI models?
**A:** 
1. Create model in `Backend/AI/`
2. Add to `model_manager.py`
3. Create API endpoint in `Backend/api/`
4. Update frontend to use new endpoint

### Q: Can I change the UI theme/colors?
**A:** Yes! Edit `FrontEnd/tailwind.config.ts` to customize:
- Colors and themes
- Component styles
- Dark/light mode settings

### Q: How do I add new charts or visualizations?
**A:** 
1. Install chart library (Recharts is already included)
2. Create component in `src/components/`
3. Connect to API data
4. Add to dashboard layout

### Q: Can I deploy this to production?
**A:** Absolutely! See deployment guides:
- **Frontend:** Build with `npm run build`, serve with nginx
- **Backend:** Use Gunicorn for production WSGI server
- **Docker:** Containerize both services
- **Cloud:** Deploy to AWS, Azure, or GCP

## 🐛 Troubleshooting

### Q: I see CORS errors in the browser console. How to fix?
**A:** Update `Backend/app.py` CORS origins:
```python
CORS(app, origins=["http://localhost:8080", "your-domain.com"])
```

### Q: Models fail to load with "FileNotFoundError". What's wrong?
**A:** 
1. Run `python setup.py` to create models
2. Check `Backend/models/` directory exists
3. Verify model files (`.pkl`) are present
4. Check file permissions

### Q: The documentation page is blank. Why?
**A:** 
1. Check browser console for JavaScript errors
2. Verify markdown files exist in `FrontEnd/public/docs/`
3. Ensure react-markdown is properly installed
4. Clear browser cache and reload

### Q: Performance is slow. How to optimize?
**A:** 
- **Backend:** Use Redis for caching, optimize model loading
- **Frontend:** Enable React production build, use code splitting
- **Database:** Add database for data persistence
- **CDN:** Serve static assets via CDN

## 📈 Advanced Usage

### Q: How do I integrate with real IoT sensors?
**A:** 
1. **Data ingestion:** Create API endpoint for sensor data
2. **Real-time processing:** Use message queues (Redis, RabbitMQ)
3. **Data validation:** Ensure sensor data matches expected format
4. **Monitoring:** Set up alerts for critical predictions

### Q: Can I train models with my own data?
**A:** Yes! 
1. **Prepare data:** Format as CSV with 24 features + targets
2. **Update training scripts:** Modify `AI/pretrained_models.py`
3. **Retrain models:** Run training with your dataset
4. **Validate performance:** Test accuracy on holdout data

### Q: How do I set up automated alerts?
**A:** 
1. **Email alerts:** Integrate with SMTP service
2. **SMS notifications:** Use Twilio or similar service
3. **Slack/Teams:** Create webhook integrations
4. **Custom actions:** Trigger maintenance workflows

### Q: Is this suitable for production use?
**A:** The system provides a solid foundation but consider:
- **Security:** Add authentication and authorization
- **Scalability:** Use load balancers and database clustering  
- **Monitoring:** Implement comprehensive logging and metrics
- **Backup:** Set up data backup and disaster recovery

## 📞 Support & Resources

### Q: Where can I get help?
**A:** 
1. **Documentation:** Check all markdown files in `/docs`
2. **Console logs:** Browser DevTools (F12) and terminal output
3. **API testing:** Use curl or Postman to test endpoints
4. **GitHub Issues:** Report bugs and feature requests

### Q: How do I contribute to the project?
**A:** 
1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request with description

### Q: Can I use this commercially?
**A:** Yes! This project uses the MIT License, allowing commercial use with proper attribution.

---

## 🎯 Quick Troubleshooting Checklist

**If something's not working:**

- [ ] Both servers running (Backend: 5000, Frontend: 8080)
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Node.js dependencies installed (`npm install`)
- [ ] Models created (`python setup.py`)
- [ ] Browser console clear of errors (F12)
- [ ] Network connectivity between frontend/backend
- [ ] Correct API URLs and ports configured
- [ ] Firewall/antivirus not blocking connections

**Still having issues?** Check the console logs, verify your setup against the project structure, and ensure all prerequisites are met.

---

🎉 **Happy monitoring!** Your predictive maintenance system should now be running smoothly.



