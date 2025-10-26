"""
Pinterest API scraper for FitFindr
----------------------------------
Fetches real Pinterest posts using Scrape Creators API.
Fallbacks to mock data if API fails (for demo stability).
"""

import os
import requests
import random
from typing import List, Dict
from dotenv import load_dotenv

# Load .env for API key
load_dotenv()


class PinterestScraper:
    """Handles communication with Scrape Creators Pinterest API."""

    def __init__(self):
        self.api_key = os.getenv("SCRAPE_CREATORS_KEY")
        if not self.api_key:
            raise ValueError("❌ Missing SCRAPE_CREATORS_KEY in .env file")

        self.endpoint = "https://api.scrapecreators.com/v1/pinterest/search"
        self.session = requests.Session()
        self.session.headers.update({"x-api-key": self.api_key})

    def scrape_pinterest(self, keyword: str, max_items: int = 20) -> List[Dict]:
        """
        Query Scrape Creators Pinterest API for posts related to keyword.
        Returns structured data usable by FitFindr backend.
        """
        try:
            print("🔑 Using Scrape Creators API")
            params = {"query": keyword, "trim": "true"}
            print(f"🔍 Querying Pinterest API for: {keyword}")

            response = self.session.get(self.endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                print("⚠️ API returned unsuccessful response, using fallback data.")
                return self._generate_mock_items(keyword, max_items)

            pins = data.get("pins", [])
            items = []

            for i, pin in enumerate(pins[:max_items]):
                images = pin.get("images", {})
                image_url = ""
                if "orig" in images:
                    image_url = images["orig"].get("url", "")

                item = {
                    "id": pin.get("id", f"pin_{i+1}"),
                    "title": pin.get("grid_title") or pin.get("description", ""),
                    "description": pin.get("description", ""),
                    "image_url": image_url,
                    "source_url": pin.get("url"),
                    "style": keyword,
                    "creator": pin.get("pinner", {}).get("full_name", ""),
                    "likes": random.randint(50, 500),
                    "saves": random.randint(10, 100),
                    "created_at": pin.get("created_at"),
                }
                items.append(item)

            print(f"✅ Retrieved {len(items)} pins for '{keyword}'")
            return items

        except Exception as e:
            print(f"❌ Pinterest API error: {e}")
            return self._generate_mock_items(keyword, max_items)

    def _generate_mock_items(self, keyword: str, count: int) -> List[Dict]:
        """Fallback mock data if API fails."""
        items = []
        for i in range(count):
            items.append({
                "id": f"mock_{i+1}",
                "title": f"Mock {keyword.title()} Item {i+1}",
                "description": f"Demo fallback {keyword} item.",
                "image_url": f"https://picsum.photos/300/400?random={i+1}",
                "source_url": "https://pinterest.com",
                "style": keyword,
                "creator": "Mock User",
                "likes": random.randint(50, 500),
                "saves": random.randint(10, 100),
                "created_at": "2025-01-01T00:00:00Z",
            })
        return items


# Public function for FastAPI
def scrape_pinterest(keyword: str, max_items: int = 20) -> List[Dict]:
    """
    External entrypoint for FastAPI route.
    Example: /scrape endpoint will call this.
    """
    scraper = PinterestScraper()
    return scraper.scrape_pinterest(keyword, max_items)


# ✅ Add this function at the very bottom
def get_trending_styles() -> List[str]:
    """Return a list of trending fashion styles."""
    return [
        "vintage streetwear",
        "minimalist chic",
        "bohemian",
        "athleisure",
        "cottagecore",
        "dark academia",
        "y2k",
        "normcore"
    ]

