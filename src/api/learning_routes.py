"""
Learning API Routes for Learning Plan 1

🎯 This file contains STUB implementations for Learning Plan 1 API exercises.
You need to complete these implementations to make the tests pass.

After implementing these routes, add them to main.py:
    from api.learning_routes import learning_router
    app.include_router(learning_router)
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Create the router
learning_router = APIRouter(prefix="/api/learning", tags=["learning"])

# You'll also need these routes without the prefix for the tests
tools_router = APIRouter(tags=["tools"])
session_router = APIRouter(tags=["sessions"])


@tools_router.get("/tools/info")
async def get_tools_info():
    """
    🧪 Exercise 4.1: Create a tool information endpoint
    
    TODO: Implement an endpoint that returns information about all available tools.
    
    Should return:
    {
        "tools": [
            {
                "name": "tool_name",
                "description": "Tool description", 
                "parameters": {"param1": "type1", "param2": "type2"},
                "examples": ["example usage"]
            },
            ...
        ]
    }
    
    You'll need to:
    1. Import your LearningEnhancedAgent
    2. Get the tools from the agent
    3. Extract tool information (name, description, parameters)
    4. Format it into a nice JSON response
    """
    # TODO: Implement tool information endpoint
    # Import your enhanced agent and get tool information
    # Look at how tools are defined in the existing agents
    
    # This is a placeholder that will make tests fail
    raise HTTPException(status_code=501, detail="You need to implement get_tools_info endpoint")


@session_router.get("/session/{session_id}/stats")
async def get_session_stats(session_id: str):
    """
    🧪 Exercise 4.2: Create a session statistics endpoint
    
    TODO: Implement an endpoint that returns statistics for a specific session.
    
    Should return:
    {
        "session_id": "session_id",
        "message_count": 5,
        "session_duration": 120.5,  # seconds
        "tools_used": ["tool1", "tool2"],
        "first_message_time": "2023-01-01T10:00:00Z",
        "last_message_time": "2023-01-01T10:02:00Z"
    }
    
    You'll need to:
    1. Import your SessionTracker
    2. Look up the session by ID
    3. Return 404 if session doesn't exist
    4. Calculate and return session statistics
    """
    # TODO: Implement session statistics endpoint
    # You'll need to integrate with your SessionTracker
    # Handle case where session doesn't exist (return 404)
    
    # This is a placeholder that will make tests fail
    raise HTTPException(status_code=501, detail="You need to implement get_session_stats endpoint")


# Export the routers so they can be included in main.py
__all__ = ["learning_router", "tools_router", "session_router"]


if __name__ == "__main__":
    print("🛠️  Learning API Routes")
    print("=" * 30)
    print()
    print("📋 Endpoints to implement:")
    print("  • GET /tools/info - List all available tools")
    print("  • GET /session/{session_id}/stats - Get session statistics")
    print()
    print("🔧 After implementing, add to main.py:")
    print("   from api.learning_routes import tools_router, session_router")
    print("   app.include_router(tools_router)")
    print("   app.include_router(session_router)")
    print()
    print("🧪 Test with:")
    print("   make test-learning PLAN=01")
    print("   Or: pytest docs/learning-plans/test_learning_01.py::TestBasicAPIExtensions -v")
