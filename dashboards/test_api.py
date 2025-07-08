#!/usr/bin/env python3
"""
Simple test script to verify the Watchtower API is working
"""

import requests
import json
import time

def test_api():
    """Test the Watchtower API endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🚁 Testing Watchtower API...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Services: {data.get('services')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test sensors endpoint
    try:
        response = requests.get(f"{base_url}/api/sensors")
        if response.status_code == 200:
            print("✅ Sensors endpoint working")
            data = response.json()
            sensors = data.get('sensors', [])
            print(f"   Found {len(sensors)} sensors:")
            for sensor in sensors:
                print(f"   - {sensor['name']}: {sensor['health']}% health")
        else:
            print(f"❌ Sensors endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Sensors error: {e}")
    
    # Test mission status
    try:
        response = requests.get(f"{base_url}/api/mission-status")
        if response.status_code == 200:
            print("✅ Mission status working")
            data = response.json()
            print(f"   Altitude: {data.get('altitude')}m")
            print(f"   Speed: {data.get('speed')}m/s")
            print(f"   Battery: {data.get('battery')}%")
        else:
            print(f"❌ Mission status failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Mission status error: {e}")
    
    # Test physics models
    try:
        response = requests.get(f"{base_url}/api/physics-models")
        if response.status_code == 200:
            print("✅ Physics models working")
            data = response.json()
            models = data.get('physics_models', {})
            print(f"   Found {len(models)} physics models:")
            for sensor_id, model in models.items():
                print(f"   - {sensor_id}: {model['name']}")
        else:
            print(f"❌ Physics models failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Physics models error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 API Test Complete!")
    print("\nIf all tests passed, you can access:")
    print("- Frontend Dashboard: http://localhost:3000")
    print("- Streamlit Dashboard: http://localhost:8501")
    print("- API Documentation: http://localhost:8000/docs")

if __name__ == "__main__":
    print("Waiting for API to start...")
    time.sleep(5)  # Give containers time to start
    test_api() 