#!/usr/bin/env python3
"""
Startup script for FitFindr backend server.
"""

import uvicorn
import sys
import os

def start_server():
    """Start the FitFindr backend server."""
    print("🚀 Starting FitFindr Backend Server")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found. Please run from backend directory.")
        sys.exit(1)
    
    print("✅ Found main.py")
    print("✅ Starting server on http://127.0.0.1:8000")
    print("✅ API documentation available at http://127.0.0.1:8000/docs")
    print("✅ Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server()
