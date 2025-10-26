"""
Recommendation engine for FitFindr.
Combines AI analysis with user preferences to generate outfit recommendations.
"""

from typing import List, Dict, Optional, Tuple
import random
from datetime import datetime

class OutfitRecommender:
    """Main recommendation engine for FitFindr."""
    
    def __init__(self):
        self.weight_fit = 0.4      # Weight for body shape compatibility
        self.weight_style = 0.3    # Weight for style preference match
        self.weight_trend = 0.2    # Weight for trending items
        self.weight_feedback = 0.1 # Weight for user feedback history
    
    def recommend_outfits(self, user_profile: Dict, available_items: List[Dict], 
                         max_recommendations: int = 10) -> List[Dict]:
        """
        Generate outfit recommendations for a user.
        
        Args:
            user_profile: User's body shape and preferences
            available_items: Available fashion items
            max_recommendations: Maximum number of recommendations
            
        Returns:
            List of recommended outfits with scores
        """
        print(f"🎯 Generating recommendations for user with {user_profile.get('body_shape', 'unknown')} body shape")
        
        # Filter items by user preferences
        filtered_items = self._filter_items_by_preferences(user_profile, available_items)
        
        if not filtered_items:
            print("⚠️ No items match user preferences, using all available items")
            filtered_items = available_items
        
        # Score each item
        scored_items = []
        for item in filtered_items:
            score_data = self._calculate_item_score(user_profile, item)
            scored_items.append({
                **item,
                **score_data,
                "recommended_at": datetime.now().isoformat()
            })
        
        # Sort by overall score and return top recommendations
        scored_items.sort(key=lambda x: x.get('overall_score', 0), reverse=True)
        
        return scored_items[:max_recommendations]
    
    def _filter_items_by_preferences(self, user_profile: Dict, items: List[Dict]) -> List[Dict]:
        """Filter items based on user preferences."""
        filtered_items = []
        
        user_style = user_profile.get('preferred_style', '').lower()
        body_shape = user_profile.get('body_shape', '').lower()
        recommended_colors = [color.lower() for color in user_profile.get('recommended_colors', [])]
        
        for item in items:
            # Style matching
            item_style = item.get('style', '').lower()
            style_match = (
                not user_style or 
                user_style in item_style or 
                item_style in user_style or
                any(keyword in item_style for keyword in user_style.split())
            )
            
            # Color matching (optional)
            item_colors = [color.lower() for color in item.get('colors', [])]
            color_match = (
                not recommended_colors or
                any(color in item_colors for color in recommended_colors) or
                any(item_color in recommended_colors for item_color in item_colors)
            )
            
            if style_match and color_match:
                filtered_items.append(item)
        
        return filtered_items
    
    def _calculate_item_score(self, user_profile: Dict, item: Dict) -> Dict:
        """Calculate compatibility scores for an item."""
        
        # Fit score based on body shape compatibility
        fit_score = self._calculate_fit_score(user_profile, item)
        
        # Style score based on preference matching
        style_score = self._calculate_style_score(user_profile, item)
        
        # Trend score based on item popularity
        trend_score = self._calculate_trend_score(item)
        
        # Feedback score based on user's previous feedback
        feedback_score = self._calculate_feedback_score(user_profile, item)
        
        # Calculate weighted overall score
        overall_score = (
            fit_score * self.weight_fit +
            style_score * self.weight_style +
            trend_score * self.weight_trend +
            feedback_score * self.weight_feedback
        )
        
        return {
            "fit_score": round(fit_score, 1),
            "style_score": round(style_score, 1),
            "trend_score": round(trend_score, 1),
            "feedback_score": round(feedback_score, 1),
            "overall_score": round(overall_score, 1),
            "explanation": self._generate_score_explanation(fit_score, style_score, overall_score),
            "styling_tips": self._generate_styling_tips(user_profile, item)
        }
    
    def _calculate_fit_score(self, user_profile: Dict, item: Dict) -> float:
        """Calculate how well the item fits the user's body shape."""
        body_shape = user_profile.get('body_shape', '').lower()
        item_category = item.get('category', '').lower()
        
        # Body shape compatibility rules
        compatibility_rules = {
            'hourglass': {
                'top': 85, 'bottom': 80, 'dress': 90, 'outerwear': 75, 'shoes': 70, 'accessories': 80
            },
            'pear': {
                'top': 90, 'bottom': 75, 'dress': 85, 'outerwear': 80, 'shoes': 75, 'accessories': 85
            },
            'apple': {
                'top': 70, 'bottom': 85, 'dress': 80, 'outerwear': 90, 'shoes': 80, 'accessories': 75
            },
            'rectangle': {
                'top': 80, 'bottom': 80, 'dress': 85, 'outerwear': 85, 'shoes': 75, 'accessories': 80
            },
            'inverted triangle': {
                'top': 75, 'bottom': 90, 'dress': 80, 'outerwear': 70, 'shoes': 80, 'accessories': 85
            }
        }
        
        base_score = compatibility_rules.get(body_shape, {}).get(item_category, 75)
        
        # Adjust based on item features
        item_title = item.get('title', '').lower()
        item_description = item.get('description', '').lower()
        
        # Positive keywords for different body shapes
        positive_keywords = {
            'hourglass': ['belted', 'wrap', 'fitted', 'cinched', 'defined'],
            'pear': ['flowy', 'a-line', 'empire', 'high-waisted', 'structured'],
            'apple': ['v-neck', 'wrap', 'a-line', 'empire', 'flowy'],
            'rectangle': ['structured', 'fitted', 'belted', 'layered', 'textured'],
            'inverted triangle': ['wide-leg', 'a-line', 'flowy', 'layered', 'textured']
        }
        
        keywords = positive_keywords.get(body_shape, [])
        keyword_bonus = sum(5 for keyword in keywords if keyword in item_title or keyword in item_description)
        
        return min(base_score + keyword_bonus, 100)
    
    def _calculate_style_score(self, user_profile: Dict, item: Dict) -> float:
        """Calculate how well the item matches user's style preferences."""
        user_style = user_profile.get('preferred_style', '').lower()
        item_style = item.get('style', '').lower()
        item_title = item.get('title', '').lower()
        item_description = item.get('description', '').lower()
        
        if not user_style:
            return 75  # Neutral score if no style preference
        
        # Direct style match
        if user_style in item_style or item_style in user_style:
            return 90
        
        # Keyword matching
        style_keywords = {
            'vintage': ['vintage', 'retro', 'classic', 'timeless', 'antique'],
            'streetwear': ['street', 'urban', 'casual', 'cool', 'edgy'],
            'formal': ['elegant', 'sophisticated', 'professional', 'refined'],
            'casual': ['relaxed', 'comfortable', 'everyday', 'easy'],
            'bohemian': ['boho', 'free-spirited', 'artistic', 'flowy'],
            'minimalist': ['clean', 'simple', 'modern', 'minimal']
        }
        
        user_keywords = style_keywords.get(user_style, [])
        matches = sum(1 for keyword in user_keywords 
                     if keyword in item_style or keyword in item_title or keyword in item_description)
        
        if matches > 0:
            return 70 + (matches * 5)  # 70-90 based on keyword matches
        
        return 60  # Low score for no matches
    
    def _calculate_trend_score(self, item: Dict) -> float:
        """Calculate trend score based on item popularity."""
        likes = item.get('likes', 0)
        saves = item.get('saves', 0)
        
        # Simple trend calculation based on engagement
        engagement_score = (likes * 0.7) + (saves * 1.3)
        
        # Normalize to 0-100 scale
        if engagement_score > 1000:
            return 100
        elif engagement_score > 500:
            return 80
        elif engagement_score > 100:
            return 60
        else:
            return 40
    
    def _calculate_feedback_score(self, user_profile: Dict, item: Dict) -> float:
        """Calculate score based on user's previous feedback."""
        # For now, return neutral score
        # In a real implementation, this would analyze user's like/dislike history
        return 75
    
    def _generate_score_explanation(self, fit_score: float, style_score: float, overall_score: float) -> str:
        """Generate explanation for the recommendation score."""
        if overall_score >= 85:
            return "Excellent match! This item perfectly complements your style and body type."
        elif overall_score >= 75:
            return "Great choice! This item works well with your preferences and body shape."
        elif overall_score >= 65:
            return "Good option! This item has potential with some styling adjustments."
        else:
            return "Consider alternatives. This item may not be the best fit for your style."
    
    def _generate_styling_tips(self, user_profile: Dict, item: Dict) -> List[str]:
        """Generate styling tips for the item."""
        body_shape = user_profile.get('body_shape', '').lower()
        item_category = item.get('category', '').lower()
        
        tips = []
        
        # General styling tips
        if item_category == 'top':
            tips.append("Tuck in for a more polished look")
            tips.append("Layer with a jacket or cardigan")
        elif item_category == 'bottom':
            tips.append("Pair with a fitted top to balance proportions")
            tips.append("Consider the right footwear for the occasion")
        elif item_category == 'outerwear':
            tips.append("Layer over a simple base")
            tips.append("Belt it for a more defined silhouette")
        
        # Body shape specific tips
        if body_shape == 'hourglass':
            tips.append("Emphasize your waist with a belt")
            tips.append("Choose fitted silhouettes that follow your curves")
        elif body_shape == 'pear':
            tips.append("Balance with a statement top")
            tips.append("Draw attention upward with accessories")
        elif body_shape == 'apple':
            tips.append("Create vertical lines with your outfit")
            tips.append("Choose pieces that skim rather than cling")
        
        return tips[:3]  # Return top 3 tips
    
    def create_outfit_combinations(self, recommendations: List[Dict]) -> List[Dict]:
        """Create complete outfit combinations from recommendations."""
        outfits = []
        
        # Group items by category
        categories = {}
        for item in recommendations:
            category = item.get('category', 'other')
            if category not in categories:
                categories[category] = []
            categories[category].append(item)
        
        # Create outfit combinations
        tops = categories.get('top', [])
        bottoms = categories.get('bottom', [])
        outerwear = categories.get('outerwear', [])
        shoes = categories.get('shoes', [])
        accessories = categories.get('accessories', [])
        
        # Generate combinations
        for i in range(min(5, len(recommendations))):  # Max 5 outfits
            outfit = {
                "outfit_id": f"outfit_{i+1}",
                "items": [],
                "total_score": 0,
                "style_cohesion": 0,
                "created_at": datetime.now().isoformat()
            }
            
            # Add one item from each category if available
            if tops:
                outfit["items"].append(random.choice(tops[:3]))
            if bottoms:
                outfit["items"].append(random.choice(bottoms[:3]))
            if outerwear:
                outfit["items"].append(random.choice(outerwear[:2]))
            if shoes:
                outfit["items"].append(random.choice(shoes[:2]))
            if accessories:
                outfit["items"].append(random.choice(accessories[:2]))
            
            # Calculate outfit metrics
            if outfit["items"]:
                scores = [item.get('overall_score', 0) for item in outfit["items"]]
                outfit["total_score"] = round(sum(scores) / len(scores), 1)
                outfit["style_cohesion"] = self._calculate_style_cohesion(outfit["items"])
            
            outfits.append(outfit)
        
        return outfits
    
    def _calculate_style_cohesion(self, items: List[Dict]) -> float:
        """Calculate how well items work together as an outfit."""
        if len(items) < 2:
            return 50
        
        # Check for style consistency
        styles = [item.get('style', '').lower() for item in items]
        unique_styles = len(set(styles))
        
        # More unique styles = lower cohesion
        cohesion_score = max(20, 100 - (unique_styles * 20))
        
        return round(cohesion_score, 1)

# Convenience functions
def recommend_outfits(user_profile: Dict, available_items: List[Dict], max_recommendations: int = 10) -> List[Dict]:
    """Main function to generate outfit recommendations."""
    recommender = OutfitRecommender()
    return recommender.recommend_outfits(user_profile, available_items, max_recommendations)

def create_outfit_combinations(recommendations: List[Dict]) -> List[Dict]:
    """Create complete outfit combinations."""
    recommender = OutfitRecommender()
    return recommender.create_outfit_combinations(recommendations)

def get_recommendation_summary(recommendations: List[Dict]) -> Dict:
    """Get summary statistics for recommendations."""
    if not recommendations:
        return {"count": 0, "average_score": 0, "top_categories": []}
    
    scores = [rec.get('overall_score', 0) for rec in recommendations]
    categories = [rec.get('category', 'other') for rec in recommendations]
    
    # Count categories
    category_counts = {}
    for category in categories:
        category_counts[category] = category_counts.get(category, 0) + 1
    
    # Sort by count
    top_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return {
        "count": len(recommendations),
        "average_score": round(sum(scores) / len(scores), 1),
        "top_categories": [cat for cat, count in top_categories],
        "score_range": {
            "min": min(scores),
            "max": max(scores)
        }
    }
