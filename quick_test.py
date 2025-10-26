#!/usr/bin/env python3
"""
Quick test script for FitFindr API
"""

import requests
import json

def quick_test():
    """Quick test of the FitFindr API"""
    base_url = "http://127.0.0.1:8000"
    
    print("Quick FitFindr API Test")
    print("=" * 40)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("SUCCESS: Server is running!")
        else:
            print(f"ERROR: Server error: {response.status_code}")
            return
    except Exception as e:
        print(f"ERROR: Cannot connect to server: {e}")
        print("TIP: Make sure to run: python start_server.py")
        return
    
    # Test 2: Process a query
    print("\nTesting user query...")
    try:
        data = {"style": "vintage streetwear"}
        response = requests.post(f"{base_url}/query", data=data)
        if response.status_code == 200:
            result = response.json()
            user_id = result['user']['id']
            print(f"SUCCESS: Query successful! User ID: {user_id}")
        else:
            print(f"ERROR: Query failed: {response.status_code}")
            return
    except Exception as e:
        print(f"ERROR: Query error: {e}")
        return
    
    # Test 3: Scrape Pinterest
    print("\nTesting Pinterest scraping...")
    try:
        payload = {"keyword": "vintage streetwear", "max_items": 10}
        response = requests.post(f"{base_url}/scrape", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"SUCCESS: Scraped {result['count']} items!")
            print(f"   Sample item: {result['items'][0]['title']}")
        else:
            print(f"ERROR: Scraping failed: {response.status_code}")
            return
    except Exception as e:
        print(f"ERROR: Scraping error: {e}")
        return
    
    # Test 4: Get recommendations
    print("\nTesting recommendations...")
    try:
        payload = {"max_recommendations": 5}
        response = requests.post(f"{base_url}/recommend", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"SUCCESS: Generated {len(result['recommendations'])} recommendations!")
            print(f"   Top recommendation: {result['recommendations'][0]['title']}")
            print(f"   Score: {result['recommendations'][0]['overall_score']}")
        else:
            print(f"ERROR: Recommendations failed: {response.status_code}")
            return
    except Exception as e:
        print(f"ERROR: Recommendations error: {e}")
        return
    
    # Test 5: Get styles
    print("\nTesting styles endpoint...")
    try:
        response = requests.get(f"{base_url}/styles")
        if response.status_code == 200:
            result = response.json()
            print(f"SUCCESS: Found {len(result['styles'])} styles!")
            print(f"   Available: {', '.join(result['styles'][:5])}...")
        else:
            print(f"ERROR: Styles failed: {response.status_code}")
    except Exception as e:
        print(f"ERROR: Styles error: {e}")
    
    print("\nAll tests completed!")
    print("TIP: Open http://127.0.0.1:8000/docs for interactive API testing")

if __name__ == "__main__":
    quick_test()
