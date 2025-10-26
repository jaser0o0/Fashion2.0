#!/usr/bin/env python3
"""
FitFindr Demo Client - Shows how to use the API programmatically
"""

import requests
import json
import time

class FitFindrClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def process_query(self, style, image_path=None):
        """Process user query with style preference"""
        print(f"🎯 Processing query for style: {style}")
        
        if image_path:
            # With image
            with open(image_path, 'rb') as f:
                files = {'image': f}
                data = {'style': style}
                response = self.session.post(f"{self.base_url}/query", data=data, files=files)
        else:
            # Without image
            data = {'style': style}
            response = self.session.post(f"{self.base_url}/query", data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Query processed successfully")
            print(f"   User ID: {result['user']['id']}")
            print(f"   Body Shape: {result['user']['body_shape_analysis']['body_shape']}")
            return result['user']
        else:
            print(f"❌ Query failed: {response.status_code}")
            return None
    
    def scrape_pinterest(self, keyword, max_items=20):
        """Scrape Pinterest for fashion items"""
        print(f"📌 Scraping Pinterest for: {keyword}")
        
        payload = {"keyword": keyword, "max_items": max_items}
        response = self.session.post(f"{self.base_url}/scrape", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Scraped {result['count']} items successfully")
            return result['items']
        else:
            print(f"❌ Scraping failed: {response.status_code}")
            return []
    
    def get_recommendations(self, max_recommendations=10):
        """Get AI-powered recommendations"""
        print(f"🤖 Getting AI recommendations...")
        
        payload = {"max_recommendations": max_recommendations}
        response = self.session.post(f"{self.base_url}/recommend", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Generated {len(result['recommendations'])} recommendations")
            print(f"✅ Created {len(result['outfits'])} outfit combinations")
            return result
        else:
            print(f"❌ Recommendations failed: {response.status_code}")
            return None
    
    def record_feedback(self, user_id, item_id, feedback_type="like"):
        """Record user feedback"""
        print(f"💬 Recording feedback: {feedback_type} for item {item_id}")
        
        payload = {
            "user_id": user_id,
            "item_id": item_id,
            "feedback_type": feedback_type
        }
        response = self.session.post(f"{self.base_url}/feedback", json=payload)
        
        if response.status_code == 200:
            print(f"✅ Feedback recorded successfully")
            return True
        else:
            print(f"❌ Feedback failed: {response.status_code}")
            return False
    
    def get_analysis(self, user_id):
        """Get AI analysis and explanations"""
        print(f"🧠 Getting AI analysis for user {user_id}")
        
        payload = {"user_id": user_id}
        response = self.session.post(f"{self.base_url}/analyze", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Analysis completed")
            print(f"   Explanation: {result['personalized_explanation'][:100]}...")
            return result
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            return None
    
    def get_trending(self):
        """Get trending items"""
        print(f"🔥 Getting trending items...")
        
        response = self.session.get(f"{self.base_url}/trending")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Found {result['count']} trending items")
            return result['trending_items']
        else:
            print(f"❌ Trending failed: {response.status_code}")
            return []
    
    def get_styles(self):
        """Get available styles"""
        print(f"🎨 Getting available styles...")
        
        response = self.session.get(f"{self.base_url}/styles")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Found {len(result['styles'])} styles")
            return result['styles']
        else:
            print(f"❌ Styles failed: {response.status_code}")
            return []

def demo_complete_flow():
    """Demonstrate the complete FitFindr flow"""
    print("🎉 FitFindr Complete Demo")
    print("=" * 50)
    
    client = FitFindrClient()
    
    # Step 1: Process user query
    user = client.process_query("vintage streetwear")
    if not user:
        print("❌ Demo failed at query step")
        return
    
    user_id = user['id']
    
    # Step 2: Scrape Pinterest
    items = client.scrape_pinterest("vintage streetwear", 15)
    if not items:
        print("❌ Demo failed at scraping step")
        return
    
    # Step 3: Get recommendations
    recommendations = client.get_recommendations(8)
    if not recommendations:
        print("❌ Demo failed at recommendations step")
        return
    
    # Step 4: Show some recommendations
    print("\n🎯 Top Recommendations:")
    for i, rec in enumerate(recommendations['recommendations'][:3], 1):
        print(f"   {i}. {rec['title']} (Score: {rec['overall_score']})")
        print(f"      Style: {rec['style']} | Category: {rec['category']}")
    
    # Step 5: Record some feedback
    if recommendations['recommendations']:
        first_item = recommendations['recommendations'][0]
        client.record_feedback(user_id, first_item['id'], "like")
    
    # Step 6: Get AI analysis
    analysis = client.get_analysis(user_id)
    if analysis:
        print(f"\n🧠 AI Analysis:")
        print(f"   {analysis['personalized_explanation']}")
    
    # Step 7: Get trending items
    trending = client.get_trending()
    
    # Step 8: Get available styles
    styles = client.get_styles()
    print(f"\n🎨 Available Styles: {', '.join(styles[:5])}...")
    
    print("\n🎉 Demo completed successfully!")
    print("=" * 50)

def demo_different_styles():
    """Demonstrate different style scraping"""
    print("\n🎨 Testing Different Styles")
    print("=" * 30)
    
    client = FitFindrClient()
    styles = ["vintage streetwear", "minimalist chic", "bohemian", "athleisure"]
    
    for style in styles:
        print(f"\n📌 Testing style: {style}")
        items = client.scrape_pinterest(style, 5)
        if items:
            print(f"   Found {len(items)} items")
            print(f"   Sample: {items[0]['title']}")

if __name__ == "__main__":
    print("🚀 FitFindr Demo Client")
    print("Make sure your server is running on http://127.0.0.1:8000")
    print()
    
    try:
        # Test server connection
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running!")
            
            # Run complete demo
            demo_complete_flow()
            
            # Test different styles
            demo_different_styles()
            
        else:
            print("❌ Server not responding")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure to start the server with: python start_server.py")
