"""
Body shape detection for FitFindr.
Analyzes body shape from images and provides styling recommendations.
"""

from typing import Dict, List, Tuple, Optional
import cv2
import numpy as np
from .analyzer import analyze_user_image

class BodyShapeDetector:
    """Detects and analyzes body shapes from images."""
    
    def __init__(self):
        self.body_shapes = {
            'hourglass': {
                'description': 'Balanced proportions with defined waist',
                'characteristics': ['defined_waist', 'balanced_bust_hips', 'curved_silhouette'],
                'styling_tips': ['emphasize_waist', 'belted_styles', 'wrap_dresses']
            },
            'pear': {
                'description': 'Wider hips than shoulders',
                'characteristics': ['narrow_shoulders', 'wider_hips', 'defined_waist'],
                'styling_tips': ['balance_with_tops', 'a_line_bottoms', 'draw_attention_up']
            },
            'apple': {
                'description': 'Wider midsection with narrower hips',
                'characteristics': ['broader_shoulders', 'wider_midsection', 'narrower_hips'],
                'styling_tips': ['create_waist_definition', 'v_necklines', 'a_line_silhouettes']
            },
            'rectangle': {
                'description': 'Straight silhouette with minimal waist definition',
                'characteristics': ['straight_silhouette', 'minimal_waist', 'balanced_proportions'],
                'styling_tips': ['create_curves', 'belted_styles', 'layered_looks']
            },
            'inverted_triangle': {
                'description': 'Broader shoulders than hips',
                'characteristics': ['broad_shoulders', 'narrow_hips', 'straight_silhouette'],
                'styling_tips': ['balance_with_bottoms', 'soften_shoulders', 'create_hip_definition']
            }
        }
    
    def detect_body_shape(self, image_data: bytes, user_style: str = "") -> Dict:
        """
        Detect body shape from image data.
        
        Args:
            image_data: Raw image bytes
            user_style: User's preferred style for context
            
        Returns:
            Body shape analysis results
        """
        print("🔍 Analyzing body shape from image...")
        
        try:
            # Use AI analyzer for body shape detection
            analysis = analyze_user_image(image_data, user_style)
            
            # Enhance with additional styling recommendations
            body_shape = analysis.get('body_shape', 'hourglass')
            enhanced_analysis = self._enhance_analysis(analysis, body_shape)
            
            print(f"✅ Body shape detected: {body_shape}")
            return enhanced_analysis
            
        except Exception as e:
            print(f"⚠️ Error in body shape detection: {e}")
            return self._get_default_analysis(user_style)
    
    def _enhance_analysis(self, base_analysis: Dict, body_shape: str) -> Dict:
        """Enhance analysis with additional styling recommendations."""
        shape_info = self.body_shapes.get(body_shape, {})
        
        enhanced = base_analysis.copy()
        enhanced.update({
            'shape_description': shape_info.get('description', ''),
            'key_characteristics': shape_info.get('characteristics', []),
            'styling_tips': shape_info.get('styling_tips', []),
            'recommended_silhouettes': self._get_recommended_silhouettes(body_shape),
            'avoid_silhouettes': self._get_avoid_silhouettes(body_shape),
            'color_recommendations': self._get_color_recommendations(body_shape),
            'accessory_tips': self._get_accessory_tips(body_shape)
        })
        
        return enhanced
    
    def _get_recommended_silhouettes(self, body_shape: str) -> List[str]:
        """Get recommended silhouettes for body shape."""
        silhouette_recommendations = {
            'hourglass': [
                'fitted', 'wrap', 'belted', 'a_line', 'pencil', 'bodycon'
            ],
            'pear': [
                'a_line', 'empire_waist', 'wrap', 'high_waisted', 'flowy_tops'
            ],
            'apple': [
                'v_neck', 'wrap', 'a_line', 'empire_waist', 'flowy', 'layered'
            ],
            'rectangle': [
                'belted', 'structured', 'layered', 'fitted', 'peplum', 'ruffled'
            ],
            'inverted_triangle': [
                'a_line', 'flowy', 'layered', 'wide_leg', 'full_skirt', 'soft_draping'
            ]
        }
        
        return silhouette_recommendations.get(body_shape, ['fitted', 'comfortable'])
    
    def _get_avoid_silhouettes(self, body_shape: str) -> List[str]:
        """Get silhouettes to avoid for body shape."""
        avoid_recommendations = {
            'hourglass': [
                'boxy', 'oversized', 'straight_cut', 'no_waist_definition'
            ],
            'pear': [
                'tight_bottoms', 'low_rise', 'clingy_materials', 'attention_to_hips'
            ],
            'apple': [
                'tight_midsection', 'high_waisted', 'belted', 'cropped_tops'
            ],
            'rectangle': [
                'straight_cut', 'no_definition', 'boxy', 'oversized'
            ],
            'inverted_triangle': [
                'broad_shoulders', 'padded_shoulders', 'wide_necklines', 'attention_to_shoulders'
            ]
        }
        
        return avoid_recommendations.get(body_shape, [])
    
    def _get_color_recommendations(self, body_shape: str) -> Dict:
        """Get color recommendations for body shape."""
        color_recommendations = {
            'hourglass': {
                'flattering': ['black', 'navy', 'burgundy', 'emerald', 'deep_red'],
                'accent_colors': ['gold', 'silver', 'jewel_tones'],
                'avoid': ['washed_out', 'too_light']
            },
            'pear': {
                'flattering': ['black', 'navy', 'dark_colors'],
                'accent_colors': ['bright_tops', 'light_bottoms'],
                'avoid': ['dark_bottoms', 'light_tops']
            },
            'apple': {
                'flattering': ['dark_colors', 'monochromatic', 'vertical_stripes'],
                'accent_colors': ['jewel_tones', 'rich_colors'],
                'avoid': ['horizontal_stripes', 'bright_midsection']
            },
            'rectangle': {
                'flattering': ['all_colors', 'contrasting', 'bold_patterns'],
                'accent_colors': ['bright', 'jewel_tones', 'metallics'],
                'avoid': ['none_specific']
            },
            'inverted_triangle': {
                'flattering': ['dark_tops', 'light_bottoms', 'monochromatic'],
                'accent_colors': ['bright_bottoms', 'patterned_bottoms'],
                'avoid': ['bright_tops', 'attention_grabbing_tops']
            }
        }
        
        return color_recommendations.get(body_shape, {
            'flattering': ['black', 'navy', 'white'],
            'accent_colors': ['jewel_tones'],
            'avoid': []
        })
    
    def _get_accessory_tips(self, body_shape: str) -> List[str]:
        """Get accessory tips for body shape."""
        accessory_tips = {
            'hourglass': [
                'Belt to emphasize waist',
                'Statement necklaces',
                'Structured bags',
                'Heels to elongate legs'
            ],
            'pear': [
                'Statement earrings',
                'Necklaces to draw attention up',
                'Structured shoulder bags',
                'Heels to balance proportions'
            ],
            'apple': [
                'Long necklaces',
                'Earrings to frame face',
                'Crossbody bags',
                'Pointed toe shoes'
            ],
            'rectangle': [
                'Bold accessories',
                'Layered necklaces',
                'Statement pieces',
                'Varied shoe styles'
            ],
            'inverted_triangle': [
                'Hip-hugging bags',
                'Bold bottom accessories',
                'Avoid shoulder bags',
                'Statement shoes'
            ]
        }
        
        return accessory_tips.get(body_shape, ['Classic accessories'])
    
    def _get_default_analysis(self, user_style: str) -> Dict:
        """Get default analysis when detection fails."""
        return {
            'body_shape': 'hourglass',
            'height_category': 'average',
            'features_to_emphasize': ['waist', 'curves'],
            'features_to_minimize': [],
            'recommended_silhouettes': ['fitted', 'wrap', 'belted'],
            'recommended_colors': ['black', 'navy', 'burgundy'],
            'confidence_score': 50,
            'shape_description': 'Balanced proportions with defined waist',
            'key_characteristics': ['defined_waist', 'balanced_bust_hips'],
            'styling_tips': ['emphasize_waist', 'belted_styles'],
            'avoid_silhouettes': ['boxy', 'oversized'],
            'color_recommendations': {
                'flattering': ['black', 'navy', 'burgundy'],
                'accent_colors': ['gold', 'silver'],
                'avoid': ['washed_out']
            },
            'accessory_tips': ['Belt to emphasize waist', 'Statement necklaces']
        }
    
    def get_styling_guide(self, body_shape: str) -> Dict:
        """Get comprehensive styling guide for body shape."""
        shape_info = self.body_shapes.get(body_shape, {})
        
        return {
            'body_shape': body_shape,
            'description': shape_info.get('description', ''),
            'characteristics': shape_info.get('characteristics', []),
            'recommended_silhouettes': self._get_recommended_silhouettes(body_shape),
            'avoid_silhouettes': self._get_avoid_silhouettes(body_shape),
            'color_guide': self._get_color_recommendations(body_shape),
            'accessory_guide': self._get_accessory_tips(body_shape),
            'outfit_suggestions': self._get_outfit_suggestions(body_shape)
        }
    
    def _get_outfit_suggestions(self, body_shape: str) -> List[Dict]:
        """Get specific outfit suggestions for body shape."""
        outfit_suggestions = {
            'hourglass': [
                {
                    'name': 'Classic Wrap Dress',
                    'description': 'Emphasizes waist and curves',
                    'items': ['wrap_dress', 'belt', 'heels', 'statement_necklace']
                },
                {
                    'name': 'Fitted Blazer + Jeans',
                    'description': 'Professional yet feminine',
                    'items': ['fitted_blazer', 'dark_jeans', 'blouse', 'pumps']
                }
            ],
            'pear': [
                {
                    'name': 'A-Line Dress',
                    'description': 'Flatters hips and creates balance',
                    'items': ['a_line_dress', 'belt', 'heels', 'earrings']
                },
                {
                    'name': 'Statement Top + Dark Bottoms',
                    'description': 'Draws attention upward',
                    'items': ['bright_top', 'dark_pants', 'heels', 'necklace']
                }
            ],
            'apple': [
                {
                    'name': 'V-Neck + A-Line Skirt',
                    'description': 'Creates vertical lines and defines waist',
                    'items': ['v_neck_top', 'a_line_skirt', 'belt', 'heels']
                },
                {
                    'name': 'Wrap Top + Wide Leg Pants',
                    'description': 'Balances proportions',
                    'items': ['wrap_top', 'wide_leg_pants', 'heels', 'long_necklace']
                }
            ],
            'rectangle': [
                {
                    'name': 'Belted Dress',
                    'description': 'Creates waist definition',
                    'items': ['shift_dress', 'wide_belt', 'heels', 'statement_earrings']
                },
                {
                    'name': 'Layered Look',
                    'description': 'Adds dimension and curves',
                    'items': ['tank_top', 'cardigan', 'jeans', 'boots']
                }
            ],
            'inverted_triangle': [
                {
                    'name': 'A-Line Dress',
                    'description': 'Balances broad shoulders',
                    'items': ['a_line_dress', 'heels', 'hip_bag', 'statement_bracelet']
                },
                {
                    'name': 'Wide Leg Pants + Fitted Top',
                    'description': 'Creates balanced proportions',
                    'items': ['fitted_top', 'wide_leg_pants', 'heels', 'long_necklace']
                }
            ]
        }
        
        return outfit_suggestions.get(body_shape, [
            {
                'name': 'Classic Look',
                'description': 'Timeless and flattering',
                'items': ['dress', 'heels', 'accessories']
            }
        ])
    
    def calculate_body_measurements(self, image_data: bytes) -> Dict:
        """
        Calculate approximate body measurements from image.
        Note: This is a simplified implementation for demo purposes.
        """
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                return self._get_default_measurements()
            
            height, width = image.shape[:2]
            
            # Simplified measurement estimation
            # In a real implementation, you would use pose detection and body landmarks
            estimated_measurements = {
                'height_estimate': height * 0.1,  # Simplified scaling
                'shoulder_width': width * 0.2,
                'waist_width': width * 0.15,
                'hip_width': width * 0.18,
                'confidence': 0.3  # Low confidence for demo
            }
            
            return estimated_measurements
            
        except Exception as e:
            print(f"Error calculating measurements: {e}")
            return self._get_default_measurements()
    
    def _get_default_measurements(self) -> Dict:
        """Get default measurements when calculation fails."""
        return {
            'height_estimate': 165,  # cm
            'shoulder_width': 40,
            'waist_width': 35,
            'hip_width': 38,
            'confidence': 0.1
        }

# Convenience functions
def detect_body_shape(image_data: bytes, user_style: str = "") -> Dict:
    """Main function to detect body shape from image."""
    detector = BodyShapeDetector()
    return detector.detect_body_shape(image_data, user_style)

def get_styling_guide(body_shape: str) -> Dict:
    """Get styling guide for specific body shape."""
    detector = BodyShapeDetector()
    return detector.get_styling_guide(body_shape)

def analyze_body_proportions(image_data: bytes) -> Dict:
    """Analyze body proportions from image."""
    detector = BodyShapeDetector()
    return detector.calculate_body_measurements(image_data)
