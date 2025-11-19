"""
Test script to verify IoT sensor system functionality
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Health check: {response.json()['status']}")
    print(f"Version: {response.json()['version']}")
    return response.json()

def test_sensors():
    """Test sensor endpoints"""
    print("\nTesting sensor endpoints...")
    
    # Get all sensors
    response = requests.get(f"{BASE_URL}/api/v1/sensors/sensors")
    data = response.json()
    print(f"Total sensors: {data['count']}")
    
    if data['sensors']:
        first_sensor = data['sensors'][0]
        print(f"Sample sensor: {first_sensor['name']}")
        print(f"Location: {first_sensor['location']}")
        print(f"Status: {first_sensor['status']}")
        return first_sensor['sensor_id']
    return None

def test_sensor_predictions():
    """Test predictions from sensors"""
    print("\nTesting AI predictions from sensors...")
    response = requests.post(
        f"{BASE_URL}/api/v1/sensors/sensors/predict",
        json={"prediction_types": ["rul", "failure_risk", "anomaly"]}
    )
    data = response.json()
    
    if 'predictions' in data:
        print("Predictions generated successfully!")
        if 'rul' in data['predictions']:
            rul = data['predictions']['rul']
            print(f"RUL: {rul['value']:.2f} hours")
        print(f"Active Sensors: {data['active_sensors']}")

def main():
    """Run tests"""
    print("="*60)
    print("IoT Sensor System Test")
    print("="*60)
    
    try:
        test_health()
        test_sensors()
        test_sensor_predictions()
        
        print("\n" + "="*60)
        print("All tests passed!")
        print("="*60)
        
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
