#!/usr/bin/env python3
"""
Quick setup script for Canvas API tutorial
Run this script to verify your Canvas API setup
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("   Please copy .env.template to .env and fill in your details")
        return False
    
    load_dotenv()
    
    required_vars = ['API_KEY', 'API_URL']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing or placeholder values in .env file:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    print("✅ Environment variables configured")
    return True

def check_packages():
    """Check if required packages are installed"""
    try:
        import canvasapi
        import requests
        import dotenv
        print("✅ Required packages installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("   Run: pip install -r requirements.txt")
        return False

def test_canvas_connection():
    """Test connection to Canvas API"""
    try:
        from canvasapi import Canvas
        
        load_dotenv()
        canvas = Canvas(os.getenv("API_URL"), os.getenv("API_KEY"))
        
        # Test API connection
        user = canvas.get_current_user()
        print(f"✅ Connected to Canvas as: {user.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Canvas connection failed: {e}")
        print("   Check your API token and course ID")
        return False

def main():
    print("🎯 Canvas API Setup Verification")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        print("\n📝 Next steps:")
        print("1. Copy .env.template to .env")
        print("2. Get your Canvas API token from Canvas Settings")
        print("3. Fill in your Canvas URL and Course ID")
        print("4. Run this script again")
        return
    
    # Check packages
    if not check_packages():
        print("\n📝 Next steps:")
        print("1. Run: pip install -r requirements.txt")
        print("2. Run this script again")
        return
    
    # Test Canvas connection
    if not test_canvas_connection():
        print("\n📝 Next steps:")
        print("1. Verify your API token is correct")
        print("2. Check your Canvas URL format")
        print("3. Make sure you have instructor access to the course")
        return
    
    print("\n🎉 Setup complete! You're ready to use the Canvas API")

if __name__ == "__main__":
    main()
