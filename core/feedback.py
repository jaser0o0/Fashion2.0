"""
Feedback system for FitFindr.
Handles user likes/dislikes and improves recommendations over time.
"""

from typing import Dict, List, Optional
from datetime import datetime
import uuid
from .storage import load_json, save_json, append_json, log_activity

class FeedbackManager:
    """Manages user feedback and recommendation improvements."""
    
    def __init__(self):
        self.feedback_types = ['like', 'dislike', 'save', 'share', 'view']
        self.importance_weights = {
            'like': 1.0,
            'dislike': -0.8,
            'save': 0.9,
            'share': 0.7,
            'view': 0.3
        }
    
    def record_feedback(self, user_id: str, item_id: str, feedback_type: str, 
                       additional_data: Dict = None) -> Dict:
        """
        Record user feedback for an item.
        
        Args:
            user_id: User's unique identifier
            item_id: Item's unique identifier
            feedback_type: Type of feedback (like, dislike, save, etc.)
            additional_data: Additional feedback data
            
        Returns:
            Feedback record
        """
        if feedback_type not in self.feedback_types:
            raise ValueError(f"Invalid feedback type. Must be one of: {self.feedback_types}")
        
        # Create feedback record
        feedback_record = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "item_id": item_id,
            "feedback_type": feedback_type,
            "timestamp": datetime.now().isoformat(),
            "importance": self.importance_weights.get(feedback_type, 0.5),
            "additional_data": additional_data or {}
        }
        
        # Save feedback
        success = append_json("feedback.json", feedback_record)
        
        if success:
            # Update user preferences based on feedback
            self._update_user_preferences(user_id, item_id, feedback_type)
            
            # Log the feedback
            log_activity("feedback_recorded", {
                "user_id": user_id,
                "item_id": item_id,
                "feedback_type": feedback_type
            })
            
            print(f"✅ Feedback recorded: {feedback_type} for item {item_id}")
        else:
            print(f"❌ Failed to record feedback: {feedback_type}")
        
        return feedback_record
    
    def _update_user_preferences(self, user_id: str, item_id: str, feedback_type: str):
        """Update user preferences based on feedback."""
        try:
            # Load user data
            users = load_json("users.json", [])
            user = next((u for u in users if u.get("id") == user_id), None)
            
            if not user:
                print(f"⚠️ User {user_id} not found for preference update")
                return
            
            # Initialize feedback history if not exists
            if "feedback_history" not in user:
                user["feedback_history"] = {
                    "liked_items": [],
                    "disliked_items": [],
                    "saved_items": [],
                    "preferred_styles": [],
                    "preferred_colors": [],
                    "preferred_categories": []
                }
            
            # Update based on feedback type
            if feedback_type == "like":
                if item_id not in user["feedback_history"]["liked_items"]:
                    user["feedback_history"]["liked_items"].append(item_id)
                # Remove from disliked if it was there
                if item_id in user["feedback_history"]["disliked_items"]:
                    user["feedback_history"]["disliked_items"].remove(item_id)
                    
            elif feedback_type == "dislike":
                if item_id not in user["feedback_history"]["disliked_items"]:
                    user["feedback_history"]["disliked_items"].append(item_id)
                # Remove from liked if it was there
                if item_id in user["feedback_history"]["liked_items"]:
                    user["feedback_history"]["liked_items"].remove(item_id)
                    
            elif feedback_type == "save":
                if item_id not in user["feedback_history"]["saved_items"]:
                    user["feedback_history"]["saved_items"].append(item_id)
            
            # Save updated user data
            save_json("users.json", users)
            
        except Exception as e:
            print(f"Error updating user preferences: {e}")
    
    def get_user_feedback_summary(self, user_id: str) -> Dict:
        """Get summary of user's feedback history."""
        feedback_data = load_json("feedback.json", [])
        user_feedback = [f for f in feedback_data if f.get("user_id") == user_id]
        
        if not user_feedback:
            return {
                "total_feedback": 0,
                "feedback_breakdown": {},
                "preferred_categories": [],
                "preferred_styles": [],
                "engagement_score": 0
            }
        
        # Calculate feedback breakdown
        feedback_breakdown = {}
        for feedback in user_feedback:
            feedback_type = feedback.get("feedback_type", "unknown")
            feedback_breakdown[feedback_type] = feedback_breakdown.get(feedback_type, 0) + 1
        
        # Calculate engagement score
        engagement_score = sum(
            feedback.get("importance", 0) for feedback in user_feedback
        )
        
        return {
            "total_feedback": len(user_feedback),
            "feedback_breakdown": feedback_breakdown,
            "engagement_score": round(engagement_score, 2),
            "last_feedback": user_feedback[-1].get("timestamp") if user_feedback else None
        }
    
    def get_item_feedback_summary(self, item_id: str) -> Dict:
        """Get summary of feedback for a specific item."""
        feedback_data = load_json("feedback.json", [])
        item_feedback = [f for f in feedback_data if f.get("item_id") == item_id]
        
        if not item_feedback:
            return {
                "total_feedback": 0,
                "feedback_breakdown": {},
                "popularity_score": 0
            }
        
        # Calculate feedback breakdown
        feedback_breakdown = {}
        total_importance = 0
        
        for feedback in item_feedback:
            feedback_type = feedback.get("feedback_type", "unknown")
            importance = feedback.get("importance", 0)
            
            feedback_breakdown[feedback_type] = feedback_breakdown.get(feedback_type, 0) + 1
            total_importance += importance
        
        # Calculate popularity score (0-100)
        popularity_score = min(100, max(0, (total_importance / len(item_feedback)) * 20))
        
        return {
            "total_feedback": len(item_feedback),
            "feedback_breakdown": feedback_breakdown,
            "popularity_score": round(popularity_score, 1)
        }
    
    def get_recommendation_improvements(self, user_id: str) -> Dict:
        """Get suggestions for improving recommendations based on feedback."""
        user_feedback = self.get_user_feedback_summary(user_id)
        
        if user_feedback["total_feedback"] < 3:
            return {
                "needs_more_feedback": True,
                "suggestions": [
                    "Like or dislike more items to improve recommendations",
                    "Save items you're interested in",
                    "Try different styles to expand your preferences"
                ]
            }
        
        # Analyze feedback patterns
        feedback_breakdown = user_feedback["feedback_breakdown"]
        likes = feedback_breakdown.get("like", 0)
        dislikes = feedback_breakdown.get("dislike", 0)
        
        suggestions = []
        
        if dislikes > likes * 2:
            suggestions.append("Consider exploring different style categories")
            suggestions.append("Try items with different silhouettes")
        
        if likes > 0 and dislikes == 0:
            suggestions.append("Great! Your preferences are clear")
            suggestions.append("Try saving items you love for future reference")
        
        return {
            "needs_more_feedback": False,
            "suggestions": suggestions,
            "feedback_quality": "good" if user_feedback["total_feedback"] >= 10 else "improving"
        }
    
    def get_trending_items(self, limit: int = 10) -> List[Dict]:
        """Get trending items based on recent feedback."""
        feedback_data = load_json("feedback.json", [])
        items_data = load_json("items.json", [])
        
        # Calculate item scores based on recent feedback
        item_scores = {}
        for feedback in feedback_data:
            item_id = feedback.get("item_id")
            if not item_id:
                continue
            
            importance = feedback.get("importance", 0)
            feedback_type = feedback.get("feedback_type", "")
            
            if item_id not in item_scores:
                item_scores[item_id] = 0
            
            item_scores[item_id] += importance
        
        # Sort by score and get top items
        sorted_items = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)
        trending_item_ids = [item_id for item_id, score in sorted_items[:limit]]
        
        # Get full item data
        trending_items = []
        for item in items_data:
            if item.get("id") in trending_item_ids:
                item["trending_score"] = item_scores.get(item["id"], 0)
                trending_items.append(item)
        
        return trending_items
    
    def analyze_feedback_patterns(self) -> Dict:
        """Analyze overall feedback patterns across all users."""
        feedback_data = load_json("feedback.json", [])
        
        if not feedback_data:
            return {
                "total_feedback": 0,
                "most_popular_feedback": "none",
                "engagement_trend": "stable"
            }
        
        # Calculate overall statistics
        feedback_types = [f.get("feedback_type", "unknown") for f in feedback_data]
        feedback_counts = {}
        for feedback_type in feedback_types:
            feedback_counts[feedback_type] = feedback_counts.get(feedback_type, 0) + 1
        
        most_popular = max(feedback_counts.items(), key=lambda x: x[1])[0]
        
        return {
            "total_feedback": len(feedback_data),
            "feedback_distribution": feedback_counts,
            "most_popular_feedback": most_popular,
            "average_importance": sum(f.get("importance", 0) for f in feedback_data) / len(feedback_data)
        }

# Convenience functions
def record_feedback(feedback_data: Dict) -> Dict:
    """Main function to record user feedback."""
    manager = FeedbackManager()
    
    user_id = feedback_data.get("user_id")
    item_id = feedback_data.get("item_id")
    feedback_type = feedback_data.get("feedback_type", "like")
    additional_data = feedback_data.get("additional_data", {})
    
    if not user_id or not item_id:
        raise ValueError("user_id and item_id are required")
    
    return manager.record_feedback(user_id, item_id, feedback_type, additional_data)

def get_user_feedback(user_id: str) -> Dict:
    """Get user's feedback summary."""
    manager = FeedbackManager()
    return manager.get_user_feedback_summary(user_id)

def get_trending_items(limit: int = 10) -> List[Dict]:
    """Get trending items."""
    manager = FeedbackManager()
    return manager.get_trending_items(limit)

def analyze_feedback_trends() -> Dict:
    """Analyze overall feedback trends."""
    manager = FeedbackManager()
    return manager.analyze_feedback_patterns()
