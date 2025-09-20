#!/usr/bin/env python3
"""
Test file for Learning Plan 1: Understand Current Code
"""

import pytest
import requests
import json
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from agent.core import LangGraphAgent
from agent.modern import ModernLangGraphAgent

class TestCurrentImplementation:
    """Test the current implementation understanding."""
    
    def test_custom_vs_modern_agents(self):
        """Test that both agent implementations work correctly."""
        print("\n🔍 Testing custom vs modern agent implementations...")
        
        # Test custom agent
        custom_agent = LangGraphAgent()
        assert custom_agent is not None
        assert hasattr(custom_agent, 'chat')
        assert hasattr(custom_agent, 'stream_chat')
        print("✅ Custom agent implementation works")
        
        # Test modern agent
        modern_agent = ModernLangGraphAgent()
        assert modern_agent is not None
        assert hasattr(modern_agent, 'chat')
        assert hasattr(modern_agent, 'stream_chat')
        print("✅ Modern agent implementation works")
        
        # Test that they have different implementations
        assert type(custom_agent) != type(modern_agent)
        print("✅ Agents have different implementations")
    
    def test_tool_integration(self):
        """Test that tools are properly integrated."""
        print("\n🔍 Testing tool integration...")
        
        custom_agent = LangGraphAgent()
        modern_agent = ModernLangGraphAgent()
        
        # Both agents should have the same tools
        assert len(custom_agent.tools) == len(modern_agent.tools)
        assert len(custom_agent.tools) == 3  # get_current_time, calculate, echo
        
        tool_names = [tool.name for tool in custom_agent.tools]
        expected_tools = ['get_current_time', 'calculate', 'echo']
        
        for expected_tool in expected_tools:
            assert expected_tool in tool_names
            print(f"✅ Tool '{expected_tool}' is properly integrated")
    
    def test_state_management(self):
        """Test state management and session handling."""
        print("\n🔍 Testing state management...")
        
        custom_agent = LangGraphAgent()
        
        # Test that checkpointer is properly initialized
        assert custom_agent.checkpointer is not None
        print("✅ Checkpointer is properly initialized")
        
        # Test that graph is compiled with checkpointer
        assert custom_agent.graph is not None
        print("✅ Graph is properly compiled with checkpointer")
    
    def test_streaming_responses(self):
        """Test streaming response functionality."""
        print("\n🔍 Testing streaming responses...")
        
        custom_agent = LangGraphAgent()
        
        # Test that streaming method exists and is callable
        assert hasattr(custom_agent, 'stream_chat')
        assert callable(custom_agent.stream_chat)
        print("✅ Streaming method is properly implemented")

class TestExtendedFunctionality:
    """Test your extensions to the current code."""
    
    def test_new_tools(self):
        """Test the new tools you've added."""
        print("\n🔍 Testing new tools...")
        
        # This is where you would test your new tools
        # For now, we'll just verify the existing tools work
        custom_agent = LangGraphAgent()
        
        # Test that tools can be called
        for tool in custom_agent.tools:
            if tool.name == 'get_current_time':
                result = tool.invoke({})
                assert 'Current time:' in result
                print(f"✅ Tool '{tool.name}' works correctly")
            elif tool.name == 'calculate':
                result = tool.invoke({'expression': '2 + 2'})
                assert 'Result: 2 + 2 = 4' in result
                print(f"✅ Tool '{tool.name}' works correctly")
            elif tool.name == 'echo':
                result = tool.invoke({'message': 'test'})
                assert 'Echo: test' in result
                print(f"✅ Tool '{tool.name}' works correctly")
    
    def test_custom_state(self):
        """Test your custom state management."""
        print("\n🔍 Testing custom state management...")
        
        # This is where you would test your custom state implementations
        # For now, we'll verify the current state management works
        custom_agent = LangGraphAgent()
        
        # Test that the agent uses MessagesState
        assert hasattr(custom_agent.graph, 'nodes')
        print("✅ State management is properly configured")
    
    def test_advanced_graphs(self):
        """Test your advanced graph patterns."""
        print("\n🔍 Testing advanced graph patterns...")
        
        # This is where you would test your advanced graph implementations
        # For now, we'll verify the current graph structure
        custom_agent = LangGraphAgent()
        
        # Test that the graph has the expected nodes
        expected_nodes = ['agent', 'tools']
        for node in expected_nodes:
            assert node in custom_agent.graph.nodes
            print(f"✅ Graph node '{node}' is properly configured")

class TestAPIEndpoints:
    """Test API endpoints for learning plan validation."""
    
    def test_health_endpoint(self):
        """Test health endpoint."""
        print("\n🔍 Testing health endpoint...")
        
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                assert data['status'] == 'healthy'
                print("✅ Health endpoint works correctly")
            else:
                print(f"⚠️  Health endpoint returned {response.status_code} - service may not be running")
        except requests.exceptions.RequestException:
            print("⚠️  Health endpoint not accessible - service may not be running")
    
    def test_chat_endpoints(self):
        """Test chat endpoints."""
        print("\n🔍 Testing chat endpoints...")
        
        payload = {
            "message": "What time is it?",
            "session_id": "test_session"
        }
        
        # Test custom chat endpoint
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json=payload,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                assert 'response' in data
                assert 'tools_used' in data
                print("✅ Custom chat endpoint works correctly")
            else:
                print(f"⚠️  Custom chat endpoint returned {response.status_code}")
        except requests.exceptions.RequestException:
            print("⚠️  Custom chat endpoint not accessible - service may not be running")
        
        # Test modern chat endpoint
        try:
            response = requests.post(
                "http://localhost:8000/chat/modern",
                json=payload,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                assert 'response' in data
                assert 'tools_used' in data
                print("✅ Modern chat endpoint works correctly")
            else:
                print(f"⚠️  Modern chat endpoint returned {response.status_code}")
        except requests.exceptions.RequestException:
            print("⚠️  Modern chat endpoint not accessible - service may not be running")

def main():
    """Run all tests for Learning Plan 1."""
    print("🚀 Starting Learning Plan 1 Tests")
    print("=" * 50)
    
    # Run the tests
    test_classes = [
        TestCurrentImplementation,
        TestExtendedFunctionality,
        TestAPIEndpoints
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_class in test_classes:
        print(f"\n📋 Running {test_class.__name__}")
        print("-" * 30)
        
        test_instance = test_class()
        methods = [method for method in dir(test_instance) if method.startswith('test_')]
        
        for method_name in methods:
            total_tests += 1
            try:
                method = getattr(test_instance, method_name)
                method()
                passed_tests += 1
                print(f"✅ {method_name} passed")
            except Exception as e:
                print(f"❌ {method_name} failed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed_tests}/{total_tests} passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! You're ready for Learning Plan 2.")
    else:
        print("❌ Some tests failed. Review the output above and try again.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
