#!/usr/bin/env python3
"""
🚨 LEARNING PLAN 1: TEST-DRIVEN UNDERSTANDING 🚨

Test file for Learning Plan 1: Understand Current Code
═══════════════════════════════════════════════════════════

❌ EXPECTED BEHAVIOR: Some tests will FAIL until you implement basic exercises
✅ THIS IS INTENTIONAL: You must prove understanding through hands-on coding

🎯 Test-Driven Learning Flow:
1. 🟢 Read existing code and understand how it works
2. 🔴 Run tests - some will fail (implementation required!)
3. 📖 Read the failing test to understand what to implement  
4. 🔧 Implement simple extensions to demonstrate understanding
5. 🔄 Run tests again - they should now pass
6. ➡️  Move to next failing test and repeat

🛠️ Quick Start:
   make test-learning PLAN=01    # See which exercises need implementation
   # Read the failures, implement the basic extensions
   # Re-run until all tests pass!

📁 Implementation Files: src/agent/learning_extensions.py, src/api/learning_routes.py
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

# Pytest fixtures for agent setup
@pytest.fixture
def custom_agent():
    """Fixture for custom LangGraph agent."""
    return LangGraphAgent()

@pytest.fixture
def modern_agent():
    """Fixture for modern LangGraph agent."""
    return ModernLangGraphAgent()

@pytest.fixture
def test_payload():
    """Fixture for API test payload."""
    return {
        "message": "What time is it?",
        "session_id": "test_session"
    }

# Test markers for different environments
pytestmark = pytest.mark.learning_plan_01

class TestCurrentImplementation:
    """Test your understanding of the existing implementation."""
    
    def test_existing_agents_work(self, custom_agent, modern_agent):
        """✅ Verify that the existing agents work correctly (should pass)."""
        # Test custom agent
        assert custom_agent is not None
        assert hasattr(custom_agent, 'chat')
        assert hasattr(custom_agent, 'stream_chat')
        
        # Test modern agent
        assert modern_agent is not None
        assert hasattr(modern_agent, 'chat')
        assert hasattr(modern_agent, 'stream_chat')
        
        # Test that they have different implementations
        assert type(custom_agent) != type(modern_agent)
    
    def test_existing_tools_work(self, custom_agent, modern_agent):
        """✅ Verify that existing tools work correctly (should pass)."""
        # Both agents should have the same tools
        assert len(custom_agent.tools) == len(modern_agent.tools)
        assert len(custom_agent.tools) == 3  # get_current_time, calculate, echo
        
        tool_names = [tool.name for tool in custom_agent.tools]
        expected_tools = ['get_current_time', 'calculate', 'echo']
        
        for expected_tool in expected_tools:
            assert expected_tool in tool_names
    
    def test_existing_state_management(self, custom_agent):
        """✅ Verify that existing state management works (should pass)."""
        # Test that checkpointer is properly initialized
        assert custom_agent.checkpointer is not None
        
        # Test that graph is compiled with checkpointer
        assert custom_agent.graph is not None

class TestBasicToolExtensions:
    """🔴 Test your basic tool extensions - THESE WILL FAIL UNTIL YOU IMPLEMENT THEM."""
    
    def test_enhanced_calculator_tool(self):
        """
        🧪 Exercise 1.1: Enhance the existing calculator tool
        
        You need to extend the calculator to support more operations:
        1. Add support for power (^) operations
        2. Add support for square root (sqrt) operations  
        3. Add support for percentage (%) operations
        4. Maintain backward compatibility
        
        📁 Implement in: src/agent/learning_extensions.py
        """
        from agent.learning_extensions import enhanced_calculate
        
        # Test existing functionality still works
        result = enhanced_calculate("2 + 3")
        assert "5" in result
        
        # Test new power operation
        result = enhanced_calculate("2 ^ 3")
        assert "8" in result
        
        # Test square root operation
        result = enhanced_calculate("sqrt(16)")
        assert "4" in result
        
        # Test percentage operation
        result = enhanced_calculate("20% of 100")
        assert "20" in result
    
    def test_new_utility_tools(self):
        """
        🧪 Exercise 1.2: Create new simple utility tools
        
        You need to create these simple tools:
        1. reverse_string(text) - reverses a string
        2. word_count(text) - counts words in text
        3. upper_lower(text, mode) - converts to upper or lower case
        
        📁 Implement in: src/agent/learning_extensions.py
        """
        from agent.learning_extensions import reverse_string, word_count, upper_lower
        
        # Test reverse_string tool
        result = reverse_string("hello")
        assert result == "olleh"
        
        # Test word_count tool
        result = word_count("hello world test")
        assert result == 3
        
        # Test upper_lower tool
        result = upper_lower("Hello World", "upper")
        assert result == "HELLO WORLD"
        
        result = upper_lower("Hello World", "lower")
        assert result == "hello world"
    
    def test_agent_with_new_tools(self):
        """
        🧪 Exercise 1.3: Create an enhanced agent with your new tools
        
        You need to create a new agent class that includes:
        1. All existing tools (get_current_time, calculate, echo)
        2. Your enhanced calculator
        3. Your new utility tools
        4. Same graph structure as existing agents
        
        📁 Implement in: src/agent/learning_extensions.py
        """
        from agent.learning_extensions import LearningEnhancedAgent
        
        agent = LearningEnhancedAgent()
        
        # Should have more tools than original
        original_agent = LangGraphAgent()
        assert len(agent.tools) > len(original_agent.tools)
        
        # Should include original tools
        tool_names = [tool.name for tool in agent.tools]
        original_tools = ['get_current_time', 'calculate', 'echo']
        for tool in original_tools:
            assert tool in tool_names
        
        # Should include new tools
        new_tools = ['enhanced_calculate', 'reverse_string', 'word_count', 'upper_lower']
        for tool in new_tools:
            assert tool in tool_names

class TestBasicStateExtensions:
    """🔴 Test your basic state understanding - THESE WILL FAIL UNTIL YOU IMPLEMENT THEM."""
    
    def test_session_state_tracker(self):
        """
        🧪 Exercise 2.1: Create a simple session state tracker
        
        You need to create a state tracker that:
        1. Tracks how many messages in a session
        2. Tracks the session start time
        3. Provides session statistics
        4. Extends MessagesState properly
        
        📁 Implement in: src/agent/learning_extensions.py
        """
        from agent.learning_extensions import SessionState, SessionTracker
        
        tracker = SessionTracker()
        
        # Test initial session creation
        session_id = "test_session_123"
        state = tracker.create_session(session_id)
        
        assert isinstance(state, SessionState)
        assert state.session_id == session_id
        assert state.message_count == 0
        assert state.start_time is not None
        
        # Test message tracking
        tracker.add_message(session_id, "Hello")
        tracker.add_message(session_id, "How are you?")
        
        stats = tracker.get_session_stats(session_id)
        assert stats["message_count"] == 2
        assert stats["session_duration"] > 0
    
    def test_message_history_analyzer(self):
        """
        🧪 Exercise 2.2: Create a message history analyzer
        
        You need to create an analyzer that:
        1. Analyzes patterns in message history
        2. Counts different message types
        3. Identifies the most used tools
        4. Provides conversation insights
        
        📁 Implement in: src/agent/learning_extensions.py
        """
        from agent.learning_extensions import MessageHistoryAnalyzer
        from langchain_core.messages import HumanMessage, AIMessage
        
        analyzer = MessageHistoryAnalyzer()
        
        # Test message analysis
        messages = [
            HumanMessage(content="What time is it?"),
            AIMessage(content="The current time is 2:30 PM"),
            HumanMessage(content="Calculate 2 + 2"),
            AIMessage(content="The result is 4")
        ]
        
        analysis = analyzer.analyze_messages(messages)
        
        assert analysis["total_messages"] == 4
        assert analysis["human_messages"] == 2
        assert analysis["ai_messages"] == 2
        assert "patterns" in analysis
        assert "tool_usage" in analysis

class TestBasicGraphExtensions:
    """🔴 Test your basic graph understanding - THESE WILL FAIL UNTIL YOU IMPLEMENT THEM."""
    
    def test_conditional_routing_graph(self):
        """
        🧪 Exercise 3.1: Create a simple conditional routing graph
        
        You need to create a graph variant that:
        1. Routes differently based on message type
        2. Has separate paths for questions vs commands
        3. Uses simple conditional logic
        4. Maintains the same basic structure
        
        📁 Implement in: src/agent/learning_extensions.py
        """
        from agent.learning_extensions import ConditionalRoutingAgent
        
        agent = ConditionalRoutingAgent()
        
        # Test that graph has conditional routing
        assert agent.graph is not None
        
        # Test different message types route differently
        question_response = agent.chat("What time is it?", "test_session")
        command_response = agent.chat("Calculate 2 + 2", "test_session")
        
        # Responses should be different (indicating different routing)
        assert question_response != command_response
    
    def test_logging_graph_wrapper(self):
        """
        🧪 Exercise 3.2: Create a simple logging wrapper for graphs
        
        You need to create a wrapper that:
        1. Logs when nodes are entered/exited
        2. Tracks execution time for each node
        3. Provides execution statistics
        4. Wraps existing graph functionality
        
        📁 Implement in: src/agent/learning_extensions.py
        """
        from agent.learning_extensions import LoggingGraphWrapper
        
        original_agent = LangGraphAgent()
        wrapped_agent = LoggingGraphWrapper(original_agent)
        
        # Test that wrapper preserves functionality
        response = wrapped_agent.chat("Hello", "test_session")
        assert response is not None
        
        # Test that logging is captured
        logs = wrapped_agent.get_execution_logs()
        assert len(logs) > 0
        assert "node_entry" in logs[0]
        assert "execution_time" in logs[0]

class TestBasicAPIExtensions:
    """🔴 Test your basic API understanding - THESE WILL FAIL UNTIL YOU IMPLEMENT THEM."""
    
    def test_tool_info_endpoint(self):
        """
        🧪 Exercise 4.1: Create a tool information endpoint
        
        You need to create an endpoint that:
        1. Lists all available tools
        2. Shows tool descriptions and parameters
        3. Provides usage examples
        4. Returns well-formatted JSON
        
        📁 Implement in: src/api/learning_routes.py
        Then add to main.py: app.include_router(learning_router)
        """
        try:
            response = requests.get("http://localhost:8000/tools/info", timeout=5)
            assert response.status_code == 200
            
            data = response.json()
            assert "tools" in data
            assert len(data["tools"]) >= 3  # At least the original tools
            
            # Each tool should have description and parameters
            for tool in data["tools"]:
                assert "name" in tool
                assert "description" in tool
                assert "parameters" in tool
        except requests.exceptions.RequestException:
            pytest.skip("Service not available - implement and start the service")
    
    def test_session_stats_endpoint(self):
        """
        🧪 Exercise 4.2: Create a session statistics endpoint
        
        You need to create an endpoint that:
        1. Shows statistics for a specific session
        2. Includes message count, duration, tools used
        3. Handles non-existent sessions gracefully
        4. Provides useful analytics
        
        📁 Implement in: src/api/learning_routes.py
        """
        try:
            # Test with existing session (create one first)
            chat_payload = {"message": "Hello", "session_id": "stats_test_session"}
            requests.post("http://localhost:8000/chat", json=chat_payload, timeout=5)
            
            # Get session stats
            response = requests.get("http://localhost:8000/session/stats_test_session/stats", timeout=5)
            assert response.status_code == 200
            
            data = response.json()
            assert "session_id" in data
            assert "message_count" in data
            assert "session_duration" in data
            assert "tools_used" in data
            
            # Test non-existent session
            response = requests.get("http://localhost:8000/session/nonexistent/stats", timeout=5)
            assert response.status_code == 404
        except requests.exceptions.RequestException:
            pytest.skip("Service not available - implement and start the service")

@pytest.mark.api
class TestExistingAPIEndpoints:
    """✅ Test existing API endpoints (should pass)."""
    
    @pytest.mark.skip_if_no_service
    def test_health_endpoint(self):
        """Test health endpoint."""
        response = requests.get("http://localhost:8000/health", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
    
    @pytest.mark.skip_if_no_service  
    def test_existing_chat_endpoints(self, test_payload):
        """Test existing chat endpoints."""
        # Test custom chat endpoint
        response = requests.post(
            "http://localhost:8000/chat",
            json=test_payload,
            timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert 'response' in data
        assert 'tools_used' in data
        
        # Test modern chat endpoint
        response = requests.post(
            "http://localhost:8000/chat/modern",
            json=test_payload,
            timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert 'response' in data
        assert 'tools_used' in data


if __name__ == "__main__":
    print()
    print("🚨" * 20)
    print("🚨  LEARNING PLAN 1: UNDERSTAND CURRENT CODE  🚨")
    print("🚨" * 20)
    print()
    print("🟢 EXISTING TESTS: Should pass (testing current functionality)")
    print("🔴 EXERCISE TESTS: Will fail until you implement them")
    print("✅ Goal: Prove your understanding through hands-on coding!")
    print()
    print("📋 Learning exercises to implement:")
    print("  1. 🛠️  Enhance existing tools (calculator with more operations)")
    print("  2. ➕ Add new utility tools (reverse_string, word_count, etc.)")
    print("  3. 🎛️  Create enhanced agents with your new tools")
    print("  4. 📊 Build session state tracking and analysis")
    print("  5. 🔀 Implement simple conditional routing")
    print("  6. 📝 Add logging and monitoring wrappers")
    print("  7. 🌐 Create new API endpoints for tool info and stats")
    print()
    print("🛠️  Implementation files to create:")
    print("   • src/agent/learning_extensions.py")
    print("   • src/api/learning_routes.py") 
    print("   • Update main.py to include new routes")
    print()
    print("🚀 Run with: pytest docs/learning-plans/test_learning_01.py -v")
    print("🚀 Or use: make test-learning PLAN=01")
    print()
    print("🚨" * 20)
