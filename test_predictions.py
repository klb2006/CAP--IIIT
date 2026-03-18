#!/usr/bin/env python3
"""
Diagnostic script to test ML model predictions with various sensor inputs
Tests different scenarios to verify model is working correctly
"""

import requests
import json
from datetime import datetime

API_URL = "https://cap-iiit-backend.onrender.com"

def test_predict(distance, temperature, water_percent, description=""):
    """Test prediction with given sensor values"""
    
    payload = {
        "distance": float(distance),
        "temperature": float(temperature),
        "water_percent": float(water_percent),
        "minute": datetime.now().minute,
        "hour": datetime.now().hour,
        "node_id": "test-node"
    }
    
    print(f"\n{'='*60}")
    print(f"Test: {description}")
    print(f"{'='*60}")
    print(f"Input:")
    print(f"  Distance: {distance} cm")
    print(f"  Temperature: {temperature} °C")
    print(f"  Water %: {water_percent} %")
    print(f"  Minute: {payload['minute']}")
    print(f"  Hour: {payload['hour']}")
    
    try:
        response = requests.post(f"{API_URL}/api/v1/predict-water", json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                print(f"\n✅ SUCCESS")
                print(f"  Predicted Water %: {result['predicted_water_percent']}")
                print(f"  Timestamp: {result['timestamp']}")
                return result['predicted_water_percent']
            else:
                print(f"\n❌ ERROR: {result['message']}")
                return None
        else:
            print(f"\n❌ HTTP Error {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ Exception: {e}")
        return None

def main():
    print("\n" + "="*60)
    print("ML MODEL PREDICTION DIAGNOSTICS")
    print("="*60)
    
    # Check API connectivity
    print("\n[1] Checking API connectivity...")
    try:
        response = requests.get(f"{API_URL}/api/v1/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print(f"✅ API is UP")
            print(f"   Model Loaded: {status['model_loaded']}")
            print(f"   Database: {status['database']}")
        else:
            print(f"❌ API returned status {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return
    
    # Test 1: Tank EMPTY
    pred1 = test_predict(
        distance=45,
        temperature=20,
        water_percent=5,
        description="Tank EMPTY (should predict LOW)"
    )
    expected1 = "LOW (< 30%)"
    
    # Test 2: Tank HALF FULL
    pred2 = test_predict(
        distance=27,
        temperature=27.5,
        water_percent=50,
        description="Tank HALF FULL (should predict MEDIUM)"
    )
    expected2 = "MEDIUM (30-70%)"
    
    # Test 3: Tank FULL
    pred3 = test_predict(
        distance=10,
        temperature=25,
        water_percent=95,
        description="Tank FULL (should predict HIGH)"
    )
    expected3 = "HIGH (> 70%)"
    
    # Test 4: Zero values (should handle gracefully)
    pred4 = test_predict(
        distance=0,
        temperature=0,
        water_percent=0,
        description="ALL ZEROS (edge case)"
    )
    
    # Print summary
    print(f"\n\n" + "="*60)
    print("PREDICTION ANALYSIS SUMMARY")
    print("="*60)
    
    print(f"\nTest 1 - Tank Empty:")
    print(f"  Expected: {expected1}")
    print(f"  Got: {pred1}")
    print(f"  Status: {'✅ PASS' if pred1 and pred1 < 30 else '⚠️ CHECK'}")
    
    print(f"\nTest 2 - Tank Half Full:")
    print(f"  Expected: {expected2}")
    print(f"  Got: {pred2}")
    print(f"  Status: {'✅ PASS' if pred2 and 30 <= pred2 <= 70 else '⚠️ CHECK'}")
    
    print(f"\nTest 3 - Tank Full:")
    print(f"  Expected: {expected3}")
    print(f"  Got: {pred3}")
    print(f"  Status: {'✅ PASS' if pred3 and pred3 > 70 else '⚠️ CHECK'}")
    
    print(f"\nTest 4 - Edge Case (zeros):")
    print(f"  Got: {pred4}")
    print(f"  Status: {'✅ HANDLED' if pred4 is not None else '❌ ERROR'}")
    
    # Check prediction history
    print(f"\n\n" + "="*60)
    print("RECENT PREDICTION HISTORY")
    print("="*60)
    
    try:
        response = requests.get(f"{API_URL}/api/v1/predictions/history?limit=5", timeout=5)
        if response.status_code == 200:
            history = response.json()
            print(f"\n✅ Last {history['count']} predictions:")
            for pred in history['data']:
                print(f"\n  ID: {pred['id']}")
                print(f"    Input: distance={pred['distance']}, temp={pred['temperature']}, water%={pred['water_percent']}")
                print(f"    Prediction: {pred['prediction']}")
                print(f"    Confidence: {pred['confidence']:.2%}")
                print(f"    Timestamp: {pred['created_at']}")
    except Exception as e:
        print(f"❌ Could not fetch history: {e}")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    main()
