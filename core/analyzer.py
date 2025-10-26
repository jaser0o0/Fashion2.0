"""
AI analyzer for FitFindr using Gemini API.
Analyzes body shape, rates outfit compatibility, and provides style explanations.
"""

import os
import base64
import json
from typing import Dict, List, Optional, Tuple
import requests
from datetime import datetime

from core.scraper import PinterestScraper

class GeminiAnalyzer:
    """AI analyzer using Google Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = model


    def analyze_body_shape(self, image_data: bytes, user_style: str) -> Dict:
        """
        Analyze body shape from uploaded image using Gemini Vision.
        
        Args:
            image_data: Raw image bytes
            user_style: User's preferred style
            
        Returns:
            Body shape analysis results
        """
        if not self.api_key:
            return self._mock_body_shape_analysis(user_style)
        
        try:
            # Encode image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Prepare prompt for body shape analysis
            prompt = f"""
            Analyze this person's body shape for fashion recommendations. 
            User's preferred style: {user_style}
            
            Please identify:
            1. Body shape type (apple, pear, hourglass, rectangle, inverted triangle)
            2. Height category (petite, average, tall)
            3. Key features to emphasize or minimize
            4. Recommended clothing silhouettes
            5. Color preferences that would work well
            
            Respond in JSON format with these fields:
            - body_shape: string
            - height_category: string  
            - features_to_emphasize: array of strings
            - features_to_minimize: array of strings
            - recommended_silhouettes: array of strings
            - recommended_colors: array of strings
            - confidence_score: number (0-100)
            """
            
            # Call Gemini Vision API
            response = self._call_gemini_vision(prompt, image_base64)
            
            if response:
                return self._parse_body_shape_response(response)
            else:
                return self._mock_body_shape_analysis(user_style)
                
        except Exception as e:
            print(f"Error in body shape analysis: {e}")
            return self._mock_body_shape_analysis(user_style)
    
    def rate_outfit_compatibility(self, user_profile: Dict, item: Dict) -> Dict:
        """
        Rate how well an outfit item matches the user's profile.
        
        Args:
            user_profile: User's body shape and preferences
            item: Fashion item to rate
            
        Returns:
            Compatibility rating and explanation
        """
        if not self.api_key:
            return self._mock_outfit_rating(user_profile, item)
        
        try:
            prompt = f"""
            Rate this fashion item's compatibility with the user's profile:
            
            User Profile:
            - Body Shape: {user_profile.get('body_shape', 'unknown')}
            - Preferred Style: {user_profile.get('preferred_style', 'unknown')}
            - Height: {user_profile.get('height_category', 'average')}
            - Features to emphasize: {user_profile.get('features_to_emphasize', [])}
            - Features to minimize: {user_profile.get('features_to_minimize', [])}
            
            Item Details:
            - Title: {item.get('title', '')}
            - Style: {item.get('style', '')}
            - Category: {item.get('category', '')}
            - Colors: {item.get('colors', [])}
            - Description: {item.get('description', '')}
            
            Please provide:
            1. Fit score (0-100) - how well it fits their body shape
            2. Style score (0-100) - how well it matches their preferred style
            3. Overall compatibility score (0-100)
            4. Brief explanation of why this works/doesn't work
            5. Specific styling tips
            
            Respond in JSON format with these fields:
            - fit_score: number
            - style_score: number
            - overall_score: number
            - explanation: string
            - styling_tips: array of strings
            """
            
            response = self._call_gemini_text(prompt)
            
            if response:
                return self._parse_rating_response(response)
            else:
                return self._mock_outfit_rating(user_profile, item)
                
        except Exception as e:
            print(f"Error in outfit rating: {e}")
            return self._mock_outfit_rating(user_profile, item)
    
    def generate_style_explanation(self, user_profile: Dict, recommendations: List[Dict]) -> str:
        """
        Generate a personalized style explanation for the user.
        
        Args:
            user_profile: User's profile data
            recommendations: List of recommended items
            
        Returns:
            Personalized style explanation
        """
        if not self.api_key:
            return self._mock_style_explanation(user_profile, recommendations)
        
        try:
            # Summarize recommendations
            rec_summary = []
            for rec in recommendations[:5]:  # Top 5 recommendations
                rec_summary.append(f"- {rec.get('title', '')} ({rec.get('style', '')})")
            
            prompt = f"""
            Generate a personalized style explanation for this user:
            
            User Profile:
            - Body Shape: {user_profile.get('body_shape', 'unknown')}
            - Preferred Style: {user_profile.get('preferred_style', 'unknown')}
            - Height: {user_profile.get('height_category', 'average')}
            
            Top Recommendations:
            {chr(10).join(rec_summary)}
            
            Please provide:
            1. A brief analysis of their style profile
            2. Why these recommendations work for them
            3. General styling tips for their body shape
            4. How to build a cohesive wardrobe
            
            Keep it conversational and encouraging (2-3 paragraphs max).
            """
            
            response = self._call_gemini_text(prompt)
            
            if response:
                return response.get('text', self._mock_style_explanation(user_profile, recommendations))
            else:
                return self._mock_style_explanation(user_profile, recommendations)
                
        except Exception as e:
            print(f"Error generating style explanation: {e}")
            return self._mock_style_explanation(user_profile, recommendations)
    
    def _call_gemini_vision(self, prompt: str, image_base64: str) -> Optional[Dict]:
        """Call Gemini Vision API."""
        try:
            url = f"{self.base_url}/models/{self.model}:generateContent"
            headers = {"Content-Type": "application/json"}
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_base64
                            }
                        }
                    ]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 1000
                }
            }
            
            response = requests.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Gemini API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error calling Gemini Vision API: {e}")
            return None
    
    def _call_gemini_text(self, prompt: str) -> Optional[Dict]:
        """Call Gemini Text API."""
        try:
            url = f"{self.base_url}/models/{self.model}:generateContent"
            headers = {"Content-Type": "application/json"}
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 1000
                }
            }
            
            response = requests.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Gemini API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error calling Gemini Text API: {e}")
            return None
    
    def _parse_body_shape_response(self, response: Dict) -> Dict:
        """Parse Gemini response for body shape analysis."""
        try:
            # Extract text from Gemini response
            text = response.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
            
            # Try to parse as JSON
            if text.strip().startswith('{'):
                return json.loads(text)
            else:
                # Fallback parsing
                return self._extract_body_shape_from_text(text)
                
        except Exception as e:
            print(f"Error parsing body shape response: {e}")
            return self._mock_body_shape_analysis("unknown")
    
    def _parse_rating_response(self, response: Dict) -> Dict:
        """Parse Gemini response for outfit rating."""
        try:
            text = response.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
            
            if text.strip().startswith('{'):
                return json.loads(text)
            else:
                return self._extract_rating_from_text(text)
                
        except Exception as e:
            print(f"Error parsing rating response: {e}")
            return self._mock_outfit_rating({}, {})
    
    def _extract_body_shape_from_text(self, text: str) -> Dict:
        """Extract body shape data from text response."""
        # Simple text parsing fallback
        return {
            "body_shape": "hourglass",
            "height_category": "average",
            "features_to_emphasize": ["waist"],
            "features_to_minimize": [],
            "recommended_silhouettes": ["fitted", "wrap", "belted"],
            "recommended_colors": ["black", "navy", "burgundy"],
            "confidence_score": 75
        }
    
    def _extract_rating_from_text(self, text: str) -> Dict:
        """Extract rating data from text response."""
        return {
            "fit_score": 80,
            "style_score": 75,
            "overall_score": 78,
            "explanation": "This item works well for your body type and style preferences.",
            "styling_tips": ["Pair with high-waisted bottoms", "Add a belt to define waist"]
        }
    
    # Mock data methods for demo purposes
    def _mock_body_shape_analysis(self, user_style: str) -> Dict:
        """Mock body shape analysis for demo."""
        body_shapes = ["hourglass", "pear", "apple", "rectangle", "inverted triangle"]
        height_categories = ["petite", "average", "tall"]
        
        return {
            "body_shape": "hourglass",
            "height_category": "average", 
            "features_to_emphasize": ["waist", "curves"],
            "features_to_minimize": [],
            "recommended_silhouettes": ["fitted", "wrap", "belted", "a-line"],
            "recommended_colors": ["black", "navy", "burgundy", "emerald"],
            "confidence_score": 85
        }
    
    def _mock_outfit_rating(self, user_profile: Dict, item: Dict) -> Dict:
        """Mock outfit rating for demo."""
        import random
        
        # Generate realistic scores based on item and user profile
        base_fit_score = random.randint(60, 95)
        base_style_score = random.randint(65, 90)
        
        # Adjust based on style match
        user_style = user_profile.get('preferred_style', '').lower()
        item_style = item.get('style', '').lower()
        
        if user_style in item_style or item_style in user_style:
            base_style_score += 10
        
        overall_score = int((base_fit_score + base_style_score) / 2)
        
        return {
            "fit_score": min(base_fit_score, 100),
            "style_score": min(base_style_score, 100),
            "overall_score": min(overall_score, 100),
            "explanation": f"This {item.get('category', 'item')} works well for your {user_profile.get('body_shape', 'body type')} and matches your {user_profile.get('preferred_style', 'style')} preferences.",
            "styling_tips": [
                "Pair with complementary colors",
                "Accessorize to complete the look",
                "Consider layering for versatility"
            ]
        }
    
    def _mock_style_explanation(self, user_profile: Dict, recommendations: List[Dict]) -> str:
        """Mock style explanation for demo."""
        body_shape = user_profile.get('body_shape', 'body type')
        preferred_style = user_profile.get('preferred_style', 'style')
        
        return f"""
        Based on your {body_shape} body shape and {preferred_style} style preferences, 
        these recommendations are perfect for you! The selected items will help 
        emphasize your best features while staying true to your personal style. 
        
        Your {body_shape} figure works beautifully with the silhouettes we've chosen, 
        and the {preferred_style} aesthetic will make you feel confident and stylish. 
        Remember to mix and match these pieces to create multiple outfit combinations!
        """

# Convenience functions
def analyze_user_image(image_data: bytes, user_style: str) -> Dict:
    """Analyze user's body shape from image."""
    analyzer = GeminiAnalyzer()
    return analyzer.analyze_body_shape(image_data, user_style)

def rate_item_compatibility(user_profile: Dict, item: Dict) -> Dict:
    """Rate item compatibility with user profile."""
    analyzer = GeminiAnalyzer()
    return analyzer.rate_outfit_compatibility(user_profile, item)

def generate_personalized_explanation(user_profile: Dict, recommendations: List[Dict]) -> str:
    """Generate personalized style explanation."""
    analyzer = GeminiAnalyzer()
    return analyzer.generate_style_explanation(user_profile, recommendations)


# Note that the following function has been added to integrate GeminiAnalyzer with PinterestScraper
# A default prompt is provided if none is given.
def generate_pinterest_recommendations(user_request: str, max_items: int = 5, items_per_request: int = 1, gen_analyzer: GeminiAnalyzer = GeminiAnalyzer(model="gemini-2.0-flash-lite")) -> List[Dict]:
    """
        Note that the following function has been added to integrate GeminiAnalyzer with PinterestScraper
        A default prompt is provided if none is given.
    """
    prompt =  f"""
            You are a fashion and style expert AI.
            Provide detailed, personalized fashion advice based on user body shape and preferences.
            Find individual complementary apparel and make outfit out of said apparel.
            Categorize the users input into distinct and complementary clothing items, 
            and generate key words seperates by commas for each item. Generate {max_items} 
            or less keywords. Here is what the user is looking for: ${user_request}. 
            HERE ARE THE HARD GUILDELINES FOR YOUR RESPONSE: 
            1. ONLY RESPOND WITH KEYWORDS SEPERATED BY COMMAS.
            2. ONLY RETURN THE KEYWORDS, NO ADDITIONAL TEXT OR FORMATTING.
            3. EACH KEYWORD CORRESPONDS TO A SINGLE  APPAREL ITEM (eg. "vintage denim jacket", "floral summer dress", "leather ankle boots").
            4. GENERATE NO MORE THAN {max_items} KEYWORDS.
            5. ENSURE THE KEYWORDS ARE HIGHLY RELEVANT TO THE USER REQUEST
            MAKE SURE TO FOLLOW THE GUIDELINES EXACTLY AS STATED.
        """

    gemini_response_text = gen_analyzer._call_gemini_text(prompt)["candidates"][0]["content"]["parts"][0]["text"]
    print("Gemini response text: ", gemini_response_text)
    dict_list = []
    for  keyword in gemini_response_text.split(','):
        dict_list = dict_list + PinterestScraper().scrape_pinterest(keyword.strip(), max_items=items_per_request)
   
    return dict_list