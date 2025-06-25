#!/usr/bin/env python3
"""
Setup script for Twitter Bot
Helps with initial configuration and testing
"""

import os
import json
import sys

def check_env_file():
    """Check if .env file exists and has required keys"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please create .env file with your API keys.")
        print("See README.md for instructions.")
        return False
    
    required_keys = [
        'OPENAI_API_KEY',
        'TWITTER_CONSUMER_KEY',
        'TWITTER_CONSUMER_SECRET',
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_TOKEN_SECRET',
        'TWITTER_BEARER_TOKEN'
    ]
    
    with open('.env', 'r') as f:
        env_content = f.read()
    
    missing_keys = []
    for key in required_keys:
        if f"{key}=" not in env_content or f"{key}=your_" in env_content:
            missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ Missing or incomplete API keys: {', '.join(missing_keys)}")
        return False
    
    print("✅ .env file looks good!")
    return True

def check_user_context():
    """Check if user_context.json is properly configured"""
    if not os.path.exists('user_context.json'):
        print("❌ user_context.json not found!")
        return False
    
    try:
        with open('user_context.json', 'r') as f:
            context = json.load(f)
        
        # Check if still has placeholder values
        if context['profile']['name'] == "Your Name":
            print("❌ Please update your profile information in user_context.json")
            return False
        
        print("✅ User context configured!")
        return True
        
    except Exception as e:
        print(f"❌ Error reading user_context.json: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    os.system("pip install -r requirements.txt")
    print("✅ Dependencies installed!")

def main():
    print("🤖 Twitter Bot Setup")
    print("=" * 40)
    
    # Check dependencies
    try:
        import openai
        import tweepy
        print("✅ Dependencies already installed")
    except ImportError:
        install_dependencies()
    
    # Check configuration
    env_ok = check_env_file()
    context_ok = check_user_context()
    
    if env_ok and context_ok:
        print("\n🎉 Setup complete! You can now run:")
        print("   python main.py test      # Test connections")
        print("   python main.py post --dry-run  # Test content generation")
        print("   python main.py post      # Post a tweet")
        print("   python main.py schedule  # Start automated posting")
    else:
        print("\n❌ Setup incomplete. Please:")
        if not env_ok:
            print("   1. Configure your API keys in .env file")
        if not context_ok:
            print("   2. Update your profile in user_context.json")
        print("\nSee README.md for detailed instructions.")

if __name__ == "__main__":
    main() 