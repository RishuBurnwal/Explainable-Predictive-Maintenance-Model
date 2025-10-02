"""
Test script for Explainable Predictive Maintenance API
Tests all endpoints with sample data
"""

import requests
import json
import numpy as np
import time
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test basic health check"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        return False

def test_api_status():
    """Test API status endpoint"""
    print("🔍 Testing API status...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data.get('status', 'unknown')}")
            print(f"   Models loaded: {data.get('models', {}).get('healthy_models', 0)}")
            return True
        else:
            print(f"❌ API status failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API status error: {e}")
        return False

def generate_sample_sensor_data():
    """Generate sample sensor data for testing"""
    # Generate realistic sensor data (24 features)
    np.random.seed(42)
    
    # 3 operational settings
    settings = np.random.normal(0, 1, 3)
    
    # 21 sensor readings
    sensors = np.random.normal(0, 1, 21)
    
    # Combine all features
    sensor_data = np.concatenate([settings, sensors]).tolist()
    
    return sensor_data

def test_rul_prediction():
    """Test RUL prediction endpoint"""
    print("🔍 Testing RUL prediction...")
    try:
        sensor_data = generate_sample_sensor_data()
        
        payload = {
            "sensor_data": sensor_data,
            "machine_id": "TEST-MACHINE-001"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/prediction/rul",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            rul = data.get('rul_prediction', 0)
            risk_level = data.get('risk_level', 'unknown')
            confidence = data.get('confidence', 0)
            
            print(f"✅ RUL Prediction successful")
            print(f"   RUL: {rul:.2f} hours")
            print(f"   Risk Level: {risk_level}")
            print(f"   Confidence: {confidence:.3f}")
            return True
        else:
            print(f"❌ RUL prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ RUL prediction error: {e}")
        return False

def test_failure_risk_prediction():
    """Test failure risk prediction endpoint"""
    print("🔍 Testing failure risk prediction...")
    try:
        sensor_data = generate_sample_sensor_data()
        
        payload = {
            "sensor_data": sensor_data,
            "machine_id": "TEST-MACHINE-001"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/prediction/failure-risk",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            risk_class = data.get('risk_class', 'unknown')
            confidence = data.get('confidence', 0)
            probabilities = data.get('probabilities', {})
            
            print(f"✅ Failure risk prediction successful")
            print(f"   Risk Class: {risk_class}")
            print(f"   Confidence: {confidence:.3f}")
            print(f"   Probabilities: {probabilities}")
            return True
        else:
            print(f"❌ Failure risk prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Failure risk prediction error: {e}")
        return False

def test_anomaly_detection():
    """Test anomaly detection endpoint"""
    print("🔍 Testing anomaly detection...")
    try:
        sensor_data = generate_sample_sensor_data()
        
        payload = {
            "sensor_data": sensor_data,
            "machine_id": "TEST-MACHINE-001"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/anomaly/detect",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            is_anomaly = data.get('is_anomaly', False)
            severity = data.get('severity', 'unknown')
            anomaly_score = data.get('anomaly_score', 0)
            
            print(f"✅ Anomaly detection successful")
            print(f"   Is Anomaly: {is_anomaly}")
            print(f"   Severity: {severity}")
            print(f"   Anomaly Score: {anomaly_score:.3f}")
            return True
        else:
            print(f"❌ Anomaly detection failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Anomaly detection error: {e}")
        return False

def test_shap_explanation():
    """Test SHAP explanation endpoint"""
    print("🔍 Testing SHAP explanation...")
    try:
        sensor_data = generate_sample_sensor_data()
        
        payload = {
            "sensor_data": sensor_data,
            "model_type": "rul",
            "machine_id": "TEST-MACHINE-001",
            "max_features": 5
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/explainability/shap",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            feature_importance = data.get('feature_importance', [])
            summary = data.get('summary', '')
            
            print(f"✅ SHAP explanation successful")
            print(f"   Top features analyzed: {len(feature_importance)}")
            print(f"   Summary: {summary}")
            
            if feature_importance:
                top_feature = feature_importance[0]
                print(f"   Most important: {top_feature['feature']} (impact: {top_feature['shap_value']:.3f})")
            
            return True
        else:
            print(f"❌ SHAP explanation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ SHAP explanation error: {e}")
        return False

def test_sample_data_generation():
    """Test sample data generation"""
    print("🔍 Testing sample data generation...")
    try:
        payload = {
            "num_samples": 10,
            "format": "json",
            "include_targets": True
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/data/generate-sample",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            samples = data.get('data', [])
            metadata = data.get('metadata', {})
            
            print(f"✅ Sample data generation successful")
            print(f"   Samples generated: {len(samples)}")
            print(f"   Features per sample: {len(metadata.get('features', []))}")
            return True
        else:
            print(f"❌ Sample data generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Sample data generation error: {e}")
        return False

def test_batch_prediction():
    """Test batch prediction endpoint"""
    print("🔍 Testing batch prediction...")
    try:
        # Generate multiple machine data
        machines = []
        for i in range(3):
            machines.append({
                "machine_id": f"TEST-MACHINE-{i+1:03d}",
                "sensor_data": generate_sample_sensor_data()
            })
        
        payload = {
            "machines": machines,
            "prediction_types": ["rul", "failure_risk", "anomaly"]
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/prediction/batch",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            successful = data.get('successful_predictions', 0)
            
            print(f"✅ Batch prediction successful")
            print(f"   Machines processed: {len(results)}")
            print(f"   Successful predictions: {successful}")
            return True
        else:
            print(f"❌ Batch prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Batch prediction error: {e}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("🚀 Starting API Tests for Explainable Predictive Maintenance")
    print("=" * 70)
    
    tests = [
        ("Health Check", test_health_check),
        ("API Status", test_api_status),
        ("RUL Prediction", test_rul_prediction),
        ("Failure Risk Prediction", test_failure_risk_prediction),
        ("Anomaly Detection", test_anomaly_detection),
        ("SHAP Explanation", test_shap_explanation),
        ("Sample Data Generation", test_sample_data_generation),
        ("Batch Prediction", test_batch_prediction)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 50)
        
        start_time = time.time()
        success = test_func()
        end_time = time.time()
        
        results.append({
            'name': test_name,
            'success': success,
            'duration': end_time - start_time
        })
        
        print(f"   Duration: {end_time - start_time:.2f}s")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    successful_tests = sum(1 for r in results if r['success'])
    total_tests = len(results)
    
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{status} {result['name']:<30} ({result['duration']:.2f}s)")
    
    print("-" * 70)
    print(f"Total: {successful_tests}/{total_tests} tests passed")
    
    if successful_tests == total_tests:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs and configuration.")
    
    return successful_tests == total_tests

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
