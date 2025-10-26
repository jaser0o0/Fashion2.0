#!/usr/bin/env python3
"""
Test script for FitFindr backend server.
"""

import requests
import json
import time

def test_server():
    """Test the FitFindr server endpoints."""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing FitFindr Backend Server")
    print("=" * 50)
    
    # Test 1: Root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False
    
    # Test 2: Styles endpoint
    try:
        response = requests.get(f"{base_url}/styles", timeout=5)
        if response.status_code == 200:
            print("✅ Styles endpoint working")
            data = response.json()
            print(f"   Available styles: {data.get('styles', [])}")
        else:
            print(f"❌ Styles endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Styles endpoint error: {e}")
    
    # Test 3: Scrape endpoint
    try:
        payload = {"keyword": "vintage streetwear", "max_items": 5}
        response = requests.post(f"{base_url}/scrape", json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Scrape endpoint working")
            data = response.json()
            print(f"   Scraped {data.get('count', 0)} items")
        else:
            print(f"❌ Scrape endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Scrape endpoint error: {e}")
    
    # Test 4: Query endpoint (without image)
    try:
        form_data = {"style": "vintage streetwear"}
        response = requests.post(f"{base_url}/query", data=form_data, timeout=10)
        if response.status_code == 200:
            print("✅ Query endpoint working")
            data = response.json()
            print(f"   User ID: {data.get('user', {}).get('id', 'N/A')}")
        else:
            print(f"❌ Query endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Query endpoint error: {e}")
    
    print("\n🎉 Server test completed!")
    return True

if __name__ == "__main__":
    test_server()
