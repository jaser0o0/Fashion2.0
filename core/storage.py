"""
Storage utilities for FitFindr backend.
Handles JSON data persistence for users, items, recommendations, and feedback.
"""

import json
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

DATA_DIR = "data"

def ensure_data_dir():
    """Ensure the data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_json(filename: str, default: Any = None) -> Any:
    """
    Load JSON data from file.
    
    Args:
        filename: Name of the JSON file
        default: Default value if file doesn't exist
        
    Returns:
        Loaded JSON data or default value
    """
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    
    if not os.path.exists(filepath):
        return default if default is not None else []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return default if default is not None else []

def save_json(filename: str, data: Any) -> bool:
    """
    Save data to JSON file.
    
    Args:
        filename: Name of the JSON file
        data: Data to save
        
    Returns:
        True if successful, False otherwise
    """
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False

def append_json(filename: str, new_data: Any) -> bool:
    """
    Append data to existing JSON array.
    
    Args:
        filename: Name of the JSON file
        new_data: New data to append
        
    Returns:
        True if successful, False otherwise
    """
    existing_data = load_json(filename, [])
    if not isinstance(existing_data, list):
        existing_data = [existing_data]
    
    existing_data.append(new_data)
    return save_json(filename, existing_data)

def get_user_by_id(user_id: str) -> Optional[Dict]:
    """Get user data by ID."""
    users = load_json("users.json", [])
    for user in users:
        if user.get("id") == user_id:
            return user
    return None

def get_items_by_style(style: str) -> List[Dict]:
    """Get items filtered by style."""
    items = load_json("items.json", [])
    return [item for item in items if style.lower() in item.get("style", "").lower()]

def get_recommendations_for_user(user_id: str) -> List[Dict]:
    """Get recommendations for a specific user."""
    recommendations = load_json("recommendations.json", [])
    return [rec for rec in recommendations if rec.get("user_id") == user_id]

def log_activity(activity: str, data: Dict = None):
    """Log activity for debugging purposes."""
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "activity": activity,
        "data": data or {}
    }
    append_json("activity_log.json", log_entry)
    print(f"[{timestamp}] {activity}")
