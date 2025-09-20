"""
Core LangGraph Agent Implementation
"""

import os
from typing import Annotated, List, Optional, Literal
from datetime import datetime
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode, create_react_agent
# Use memory checkpointing for now - Redis checkpointing may not be available in all versions
from langgraph.graph.message import MessagesState

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

class LangGraphAgent:
    """Main LangGraph Agent class using modern patterns."""
    
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
        
        # Create the graph using modern patterns
        self.graph = self._create_graph()
    
    def _create_graph(self) -> StateGraph:
        """Create the LangGraph workflow using modern patterns."""
        # Use MessagesState for better message handling
        workflow = StateGraph(MessagesState)
        
        # Bind tools to LLM
        llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Define the agent node
        def call_model(state: MessagesState):
            messages = state['messages']
            response = llm_with_tools.invoke(messages)
            return {"messages": [response]}
        
        # Define tool node
        tool_node = ToolNode(self.tools)
        
        # Define conditional logic
        def should_continue(state: MessagesState) -> Literal["tools", END]:
            messages = state['messages']
            last_message = messages[-1]
            if last_message.tool_calls:
                return "tools"
            return END
        
        # Add nodes
        workflow.add_node("agent", call_model)
        workflow.add_node("tools", tool_node)
        
        # Add edges
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "tools": "tools",
                END: END
            }
        )
        workflow.add_edge("tools", "agent")
        
        return workflow.compile(checkpointer=self.checkpointer)
    
    def chat(self, user_input: str, session_id: str = "default") -> dict:
        """Process a chat message."""
        messages = [HumanMessage(content=user_input)]
        
        result = self.graph.invoke(
            {"messages": messages}, 
            {"configurable": {"thread_id": session_id}}
        )
        
        # Extract response and metadata
        last_message = result["messages"][-1]
        response_content = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # Track tools used
        tools_used = []
        for message in result["messages"]:
            if hasattr(message, 'tool_calls') and message.tool_calls:
                for tool_call in message.tool_calls:
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
        messages = [HumanMessage(content=user_input)]
        
        return self.graph.stream(
            {"messages": messages}, 
            {"configurable": {"thread_id": session_id}}
        )
