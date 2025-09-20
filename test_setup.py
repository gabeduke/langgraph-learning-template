#!/usr/bin/env python3
"""
Test script to verify the setup works
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from src.agent.core import LangGraphAgent
        print("✅ Core agent import successful")
    except Exception as e:
        print(f"❌ Core agent import failed: {e}")
        return False
    
    try:
        from src.agent.modern import ModernLangGraphAgent
        print("✅ Modern agent import successful")
    except Exception as e:
        print(f"❌ Modern agent import failed: {e}")
        return False
    
    try:
        from src.api.routes import app
        print("✅ API routes import successful")
    except Exception as e:
        print(f"❌ API routes import failed: {e}")
        return False
    
    return True

def test_agent_creation():
    """Test that agents can be created."""
    print("\n🔍 Testing agent creation...")
    
    try:
        from src.agent.core import LangGraphAgent
        agent = LangGraphAgent()
        print("✅ Core agent creation successful")
    except Exception as e:
        print(f"❌ Core agent creation failed: {e}")
        return False
    
    try:
        from src.agent.modern import ModernLangGraphAgent
        modern_agent = ModernLangGraphAgent()
        print("✅ Modern agent creation successful")
    except Exception as e:
        print(f"❌ Modern agent creation failed: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("🚀 Testing LangGraph Agent Setup")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_agent_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! The setup is working correctly.")
        print("\nNext steps:")
        print("1. Set your OpenAI API key in .env file")
        print("2. Run: python main.py")
        print("3. Or run: docker-compose up")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
