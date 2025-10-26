"""
Query handler for FitFindr.
Processes user queries and coordinates between different modules.
"""

from typing import Dict, Optional, Tuple
import uuid
from datetime import datetime
from .analyzer import analyze_user_image
from .storage import save_json, log_activity

class QueryProcessor:
    """Main query processor for handling user requests."""
    
    def __init__(self):
        self.supported_image_formats = ['jpg', 'jpeg', 'png', 'webp']
        self.max_image_size = 10 * 1024 * 1024  # 10MB
    
    async def process_query(self, style: str, image_data: Optional[bytes] = None) -> Dict:
        """
        Process a user query with style preference and optional image.
        
        Args:
            style: User's preferred style (e.g., "vintage streetwear")
            image_data: Optional image bytes for body shape analysis
            
        Returns:
            Processed user data with analysis results
        """
        print(f"🔍 Processing query for style: {style}")
        
        # Generate unique user ID
        user_id = str(uuid.uuid4())
        
        # Initialize user data
        user_data = {
            "id": user_id,
            "preferred_style": style,
            "created_at": datetime.now().isoformat(),
            "body_shape_analysis": None,
            "image_uploaded": image_data is not None,
            "query_processed": True
        }
        
        # Process image if provided
        if image_data:
            print("📸 Analyzing uploaded image for body shape...")
            try:
                body_analysis = analyze_user_image(image_data, style)
                user_data["body_shape_analysis"] = body_analysis
                print(f"✅ Body shape detected: {body_analysis.get('body_shape', 'unknown')}")
            except Exception as e:
                print(f"⚠️ Error analyzing image: {e}")
                user_data["body_shape_analysis"] = self._get_default_body_analysis(style)
        else:
            print("📝 No image provided, using default body shape analysis")
            user_data["body_shape_analysis"] = self._get_default_body_analysis(style)
        
        # Log the query processing
        log_activity("query_processed", {
            "user_id": user_id,
            "style": style,
            "has_image": image_data is not None,
            "body_shape": user_data["body_shape_analysis"].get("body_shape")
        })
        
        return user_data
    
    def _get_default_body_analysis(self, style: str) -> Dict:
        """Get default body shape analysis when no image is provided."""
        # Style-based default assumptions
        style_defaults = {
            "vintage": {
                "body_shape": "hourglass",
                "height_category": "average",
                "features_to_emphasize": ["waist", "curves"],
                "features_to_minimize": [],
                "recommended_silhouettes": ["fitted", "wrap", "belted", "a-line"],
                "recommended_colors": ["black", "navy", "burgundy", "emerald", "cream"],
                "confidence_score": 60
            },
            "streetwear": {
                "body_shape": "rectangle",
                "height_category": "average",
                "features_to_emphasize": ["shoulders", "legs"],
                "features_to_minimize": [],
                "recommended_silhouettes": ["oversized", "relaxed", "structured"],
                "recommended_colors": ["black", "white", "gray", "navy", "olive"],
                "confidence_score": 60
            },
            "formal": {
                "body_shape": "hourglass",
                "height_category": "average",
                "features_to_emphasize": ["waist", "shoulders"],
                "features_to_minimize": [],
                "recommended_silhouettes": ["fitted", "structured", "tailored"],
                "recommended_colors": ["black", "navy", "gray", "white", "burgundy"],
                "confidence_score": 60
            },
            "casual": {
                "body_shape": "rectangle",
                "height_category": "average",
                "features_to_emphasize": ["comfort", "versatility"],
                "features_to_minimize": [],
                "recommended_silhouettes": ["relaxed", "comfortable", "easy"],
                "recommended_colors": ["blue", "white", "gray", "beige", "black"],
                "confidence_score": 60
            }
        }
        
        # Find matching style or use default
        style_lower = style.lower()
        for style_key, defaults in style_defaults.items():
            if style_key in style_lower:
                return defaults
        
        # Default fallback
        return {
            "body_shape": "hourglass",
            "height_category": "average",
            "features_to_emphasize": ["waist"],
            "features_to_minimize": [],
            "recommended_silhouettes": ["fitted", "comfortable"],
            "recommended_colors": ["black", "navy", "white"],
            "confidence_score": 50
        }
    
    def validate_style_input(self, style: str) -> Tuple[bool, str]:
        """
        Validate user's style input.
        
        Args:
            style: User's style preference
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not style or not style.strip():
            return False, "Style preference is required"
        
        if len(style) < 2:
            return False, "Style preference must be at least 2 characters"
        
        if len(style) > 100:
            return False, "Style preference must be less than 100 characters"
        
        # Check for valid characters
        if not style.replace(' ', '').replace('-', '').replace('&', '').isalnum():
            return False, "Style preference contains invalid characters"
        
        return True, ""
    
    def validate_image(self, image_data: bytes, filename: str = None) -> Tuple[bool, str]:
        """
        Validate uploaded image.
        
        Args:
            image_data: Image bytes
            filename: Original filename
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file size
        if len(image_data) > self.max_image_size:
            return False, f"Image too large. Maximum size is {self.max_image_size // (1024*1024)}MB"
        
        # Check file format
        if filename:
            file_extension = filename.split('.')[-1].lower()
            if file_extension not in self.supported_image_formats:
                return False, f"Unsupported image format. Supported: {', '.join(self.supported_image_formats)}"
        
        # Basic image validation (check for common image headers)
        if not self._is_valid_image_data(image_data):
            return False, "Invalid image data"
        
        return True, ""
    
    def _is_valid_image_data(self, image_data: bytes) -> bool:
        """Basic validation of image data."""
        # Check for common image file signatures
        image_signatures = [
            b'\xff\xd8\xff',  # JPEG
            b'\x89PNG\r\n\x1a\n',  # PNG
            b'RIFF',  # WebP (partial)
            b'GIF87a',  # GIF
            b'GIF89a',  # GIF
        ]
        
        for signature in image_signatures:
            if image_data.startswith(signature):
                return True
        
        return False
    
    def extract_style_keywords(self, style: str) -> list:
        """
        Extract keywords from style preference.
        
        Args:
            style: User's style preference
            
        Returns:
            List of extracted keywords
        """
        # Common style keywords
        style_keywords = [
            'vintage', 'retro', 'classic', 'timeless',
            'streetwear', 'urban', 'casual', 'cool',
            'formal', 'elegant', 'sophisticated',
            'bohemian', 'boho', 'free-spirited',
            'minimalist', 'clean', 'simple',
            'romantic', 'feminine', 'girly',
            'edgy', 'alternative', 'punk',
            'preppy', 'academic', 'ivy',
            'sporty', 'athletic', 'active',
            'artistic', 'creative', 'unique'
        ]
        
        style_lower = style.lower()
        found_keywords = []
        
        for keyword in style_keywords:
            if keyword in style_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def get_style_suggestions(self, partial_style: str) -> list:
        """
        Get style suggestions based on partial input.
        
        Args:
            partial_style: Partial style input
            
        Returns:
            List of style suggestions
        """
        all_styles = [
            "vintage streetwear",
            "minimalist chic",
            "bohemian",
            "athleisure",
            "cottagecore",
            "dark academia",
            "y2k",
            "normcore",
            "preppy",
            "grunge",
            "romantic",
            "edgy",
            "casual chic",
            "business casual",
            "evening wear"
        ]
        
        partial_lower = partial_style.lower()
        suggestions = []
        
        for style in all_styles:
            if partial_lower in style.lower():
                suggestions.append(style)
        
        return suggestions[:5]  # Return top 5 suggestions

# Convenience functions
async def process_query(style: str, image_data: Optional[bytes] = None) -> Dict:
    """Main function to process user queries."""
    processor = QueryProcessor()
    return await processor.process_query(style, image_data)

def validate_user_input(style: str, image_data: Optional[bytes] = None, filename: str = None) -> Tuple[bool, str]:
    """Validate user input."""
    processor = QueryProcessor()
    
    # Validate style
    is_valid_style, style_error = processor.validate_style_input(style)
    if not is_valid_style:
        return False, style_error
    
    # Validate image if provided
    if image_data:
        is_valid_image, image_error = processor.validate_image(image_data, filename)
        if not is_valid_image:
            return False, image_error
    
    return True, ""

def get_style_recommendations(style: str) -> Dict:
    """Get style recommendations and keywords."""
    processor = QueryProcessor()
    
    keywords = processor.extract_style_keywords(style)
    suggestions = processor.get_style_suggestions(style)
    
    return {
        "original_style": style,
        "extracted_keywords": keywords,
        "suggestions": suggestions,
        "is_valid": len(keywords) > 0
    }
