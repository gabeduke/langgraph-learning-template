"""
Learning Extensions for Learning Plan 1

🎯 This file contains STUB implementations for Learning Plan 1 exercises.
You need to complete these implementations to make the tests pass.

The tests in test_learning_01.py will fail until you properly implement these functions and classes.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import time
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import MessagesState
from agent.core import LangGraphAgent


def enhanced_calculate(expression: str) -> str:
    """
    🧪 Exercise 1.1: Enhance the calculator tool
    
    TODO: Extend the existing calculator to support:
    - Power operations (^): "2 ^ 3" should return "8"
    - Square root operations: "sqrt(16)" should return "4"  
    - Percentage operations: "20% of 100" should return "20"
    - Keep existing functionality for +, -, *, /
    
    Args:
        expression: Mathematical expression as string
        
    Returns:
        String with the calculation result
    """
    # TODO: Implement enhanced calculator logic
    # You can use the existing calculate tool as a starting point
    # Look at src/agent/core.py to see how the original calculate tool works
    
    # This is a placeholder that will make tests fail
    raise NotImplementedError("You need to implement enhanced_calculate function")


def reverse_string(text: str) -> str:
    """
    🧪 Exercise 1.2a: Create reverse_string utility tool
    
    TODO: Create a simple function that reverses a string.
    
    Args:
        text: String to reverse
        
    Returns:
        Reversed string
    """
    # TODO: Implement string reversal
    # Hint: Python strings can be sliced with [::-1]
    
    raise NotImplementedError("You need to implement reverse_string function")


def word_count(text: str) -> int:
    """
    🧪 Exercise 1.2b: Create word_count utility tool
    
    TODO: Create a function that counts words in text.
    
    Args:
        text: Text to count words in
        
    Returns:
        Number of words
    """
    # TODO: Implement word counting
    # Hint: You can split on whitespace and count the parts
    
    raise NotImplementedError("You need to implement word_count function")


def upper_lower(text: str, mode: str) -> str:
    """
    🧪 Exercise 1.2c: Create upper_lower case conversion tool
    
    TODO: Create a function that converts text case.
    
    Args:
        text: Text to convert
        mode: "upper" or "lower"
        
    Returns:
        Converted text
    """
    # TODO: Implement case conversion
    # Handle both "upper" and "lower" modes
    
    raise NotImplementedError("You need to implement upper_lower function")


class LearningEnhancedAgent:
    """
    🧪 Exercise 1.3: Create an enhanced agent with new tools
    
    TODO: Create an agent class that includes all existing tools plus your new ones.
    
    This should:
    1. Include all tools from the original LangGraphAgent
    2. Add your enhanced_calculate tool
    3. Add your utility tools (reverse_string, word_count, upper_lower)
    4. Use the same graph structure as the original
    """
    
    def __init__(self):
        # TODO: Initialize the enhanced agent
        # Look at src/agent/core.py to see how LangGraphAgent is implemented
        # You'll need to create tools and build a graph
        
        self.tools = []  # TODO: Add all tools here
        self.graph = None  # TODO: Build the graph
        
        # This is a placeholder that will make tests fail
        raise NotImplementedError("You need to implement LearningEnhancedAgent.__init__")


class SessionState(MessagesState):
    """
    🧪 Exercise 2.1a: Create a session state that extends MessagesState
    
    TODO: Add session tracking fields to the basic MessagesState.
    """
    
    # TODO: Add additional fields for session tracking
    # Hint: You'll need session_id, message_count, start_time, etc.
    
    def __init__(self, **kwargs):
        # TODO: Initialize the session state
        # Call parent constructor and add your fields
        super().__init__(**kwargs)
        
        # This is a placeholder that will make tests fail
        raise NotImplementedError("You need to implement SessionState.__init__")


class SessionTracker:
    """
    🧪 Exercise 2.1b: Create a session tracker
    
    TODO: Create a class that tracks session statistics.
    """
    
    def __init__(self):
        # TODO: Initialize session tracking
        # You'll need to store session data somewhere
        
        # This is a placeholder that will make tests fail
        self.sessions = {}
    
    def create_session(self, session_id: str) -> SessionState:
        """Create a new session and return its state."""
        # TODO: Create a new session with the given ID
        # Return a SessionState object
        
        raise NotImplementedError("You need to implement create_session method")
    
    def add_message(self, session_id: str, message: str) -> None:
        """Add a message to the session."""
        # TODO: Track a new message in the session
        # Update message count and any other relevant stats
        
        raise NotImplementedError("You need to implement add_message method")
    
    def get_session_stats(self, session_id: str) -> Dict[str, Any]:
        """Get statistics for a session."""
        # TODO: Return session statistics
        # Should include message_count, session_duration, etc.
        
        raise NotImplementedError("You need to implement get_session_stats method")


class MessageHistoryAnalyzer:
    """
    🧪 Exercise 2.2: Create a message history analyzer
    
    TODO: Create a class that analyzes message patterns.
    """
    
    def __init__(self):
        # TODO: Initialize the analyzer
        pass
    
    def analyze_messages(self, messages: List[BaseMessage]) -> Dict[str, Any]:
        """
        Analyze a list of messages and return insights.
        
        Should return:
        - total_messages: int
        - human_messages: int  
        - ai_messages: int
        - patterns: dict (any patterns you detect)
        - tool_usage: dict (tool usage statistics)
        """
        # TODO: Implement message analysis
        # Count different message types
        # Look for patterns in the messages
        # Analyze tool usage if present
        
        raise NotImplementedError("You need to implement analyze_messages method")


class ConditionalRoutingAgent:
    """
    🧪 Exercise 3.1: Create a conditional routing agent
    
    TODO: Create an agent that routes differently based on message type.
    """
    
    def __init__(self):
        # TODO: Create an agent with conditional routing
        # Look at how the original agent creates its graph
        # Add conditional logic to route questions vs commands differently
        
        self.graph = None
        
        raise NotImplementedError("You need to implement ConditionalRoutingAgent.__init__")
    
    def chat(self, message: str, session_id: str) -> str:
        """Chat with conditional routing based on message type."""
        # TODO: Implement chat with your conditional routing graph
        
        raise NotImplementedError("You need to implement chat method")


class LoggingGraphWrapper:
    """
    🧪 Exercise 3.2: Create a logging wrapper for graphs
    
    TODO: Create a wrapper that logs graph execution.
    """
    
    def __init__(self, original_agent: LangGraphAgent):
        # TODO: Wrap the original agent with logging
        # Store the original agent and initialize logging
        
        self.original_agent = original_agent
        self.execution_logs = []
        
        raise NotImplementedError("You need to implement LoggingGraphWrapper.__init__")
    
    def chat(self, message: str, session_id: str) -> str:
        """Chat with logging wrapper."""
        # TODO: Implement chat with logging
        # Log when nodes are entered/exited
        # Track execution time
        # Call the original agent's chat method
        
        raise NotImplementedError("You need to implement chat method")
    
    def get_execution_logs(self) -> List[Dict[str, Any]]:
        """Get the execution logs."""
        # TODO: Return the logs you've captured
        # Each log entry should have node_entry, execution_time, etc.
        
        raise NotImplementedError("You need to implement get_execution_logs method")
