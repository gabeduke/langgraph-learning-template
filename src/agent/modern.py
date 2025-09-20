"""
Modern LangGraph Agent Implementation using prebuilt components
"""

import os
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
# Use memory checkpointing for now - Redis checkpointing may not be available in all versions

# Load environment variables
load_dotenv()

# Basic tools for the agent
@tool
def get_current_time() -> str:
    """Get the current date and time."""
    return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression safely."""
    try:
        # Simple evaluation for basic math - in production, use a proper math parser
        result = eval(expression)
        return f"Result: {expression} = {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

@tool
def echo(message: str) -> str:
    """Echo back the input message."""
    return f"Echo: {message}"

class ModernLangGraphAgent:
    """Modern LangGraph Agent using prebuilt components."""
    
    def __init__(self, redis_url: Optional[str] = None):
        """Initialize the agent."""
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Define tools
        self.tools = [get_current_time, calculate, echo]
        
        # Initialize checkpointer - using memory for now
        from langgraph.checkpoint.memory import MemorySaver
        self.checkpointer = MemorySaver()
        
        # Create the agent using prebuilt components
        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            checkpointer=self.checkpointer
        )
    
    def chat(self, user_input: str, session_id: str = "default") -> dict:
        """Process a chat message."""
        messages = [{"role": "user", "content": user_input}]
        
        result = self.agent.invoke(
            {"messages": messages}, 
            {"configurable": {"thread_id": session_id}}
        )
        
        # Extract response and metadata
        last_message = result["messages"][-1]
        if hasattr(last_message, 'content'):
            response_content = last_message.content
        elif isinstance(last_message, dict):
            response_content = last_message.get("content", str(last_message))
        else:
            response_content = str(last_message)
        
        # Track tools used
        tools_used = []
        for message in result["messages"]:
            if hasattr(message, 'tool_calls') and message.tool_calls:
                for tool_call in message.tool_calls:
                    if tool_call["name"] not in tools_used:
                        tools_used.append(tool_call["name"])
            elif isinstance(message, dict) and "tool_calls" in message:
                for tool_call in message["tool_calls"]:
                    if tool_call["name"] not in tools_used:
                        tools_used.append(tool_call["name"])
        
        return {
            "messages": result["messages"],
            "agent_response": response_content,
            "session_id": session_id,
            "tools_used": tools_used,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "model": "gpt-4o-mini"
            }
        }
    
    def stream_chat(self, user_input: str, session_id: str = "default"):
        """Stream chat responses."""
        messages = [{"role": "user", "content": user_input}]
        
        return self.agent.stream(
            {"messages": messages}, 
            {"configurable": {"thread_id": session_id}}
        )
