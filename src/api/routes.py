"""
FastAPI routes for the agent API
"""

import os
import uuid
from datetime import datetime
from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import json

from .models import ChatRequest, ChatResponse, HealthResponse, StreamChunk
from ..agent.core import LangGraphAgent
from ..agent.modern import ModernLangGraphAgent

# Initialize FastAPI app
app = FastAPI(
    title="LangGraph Agent API",
    description="A generic LangGraph agent framework",
    version="1.0.0"
)

# Initialize agents
redis_url = os.getenv("REDIS_URL")
agent = LangGraphAgent(redis_url=redis_url)
modern_agent = ModernLangGraphAgent(redis_url=redis_url)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the agent (custom implementation)."""
    try:
        session_id = request.session_id or str(uuid.uuid4())
        result = agent.chat(request.message, session_id)
        
        return ChatResponse(
            response=result["agent_response"],
            session_id=session_id,
            tools_used=result.get("tools_used", []),
            metadata=result.get("metadata", {}),
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/modern", response_model=ChatResponse)
async def chat_modern(request: ChatRequest):
    """Chat with the modern agent (using prebuilt components)."""
    try:
        session_id = request.session_id or str(uuid.uuid4())
        result = modern_agent.chat(request.message, session_id)
        
        return ChatResponse(
            response=result["agent_response"],
            session_id=session_id,
            tools_used=result.get("tools_used", []),
            metadata=result.get("metadata", {}),
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def stream_chat(request: ChatRequest):
    """Stream chat responses (custom implementation)."""
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        async def generate_stream():
            for chunk in agent.stream_chat(request.message, session_id):
                if "agent" in chunk:
                    agent_data = chunk["agent"]
                    if "messages" in agent_data:
                        last_message = agent_data["messages"][-1]
                        if hasattr(last_message, 'content') and last_message.content:
                            yield f"data: {json.dumps({'chunk_type': 'agent', 'content': last_message.content})}\n\n"
                
                if "tools" in chunk:
                    yield f"data: {json.dumps({'chunk_type': 'tools', 'content': 'Executing tools...'})}\n\n"
            
            yield f"data: {json.dumps({'chunk_type': 'end', 'content': 'Stream complete'})}\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream/modern")
async def stream_chat_modern(request: ChatRequest):
    """Stream chat responses (modern implementation)."""
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        async def generate_stream():
            for chunk in modern_agent.stream_chat(request.message, session_id):
                if "agent" in chunk:
                    agent_data = chunk["agent"]
                    if "messages" in agent_data:
                        last_message = agent_data["messages"][-1]
                        if hasattr(last_message, 'content') and last_message.content:
                            yield f"data: {json.dumps({'chunk_type': 'agent', 'content': last_message.content})}\n\n"
                
                if "tools" in chunk:
                    yield f"data: {json.dumps({'chunk_type': 'tools', 'content': 'Executing tools...'})}\n\n"
            
            yield f"data: {json.dumps({'chunk_type': 'end', 'content': 'Stream complete'})}\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "LangGraph Agent API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "chat_modern": "/chat/modern",
            "stream": "/chat/stream",
            "stream_modern": "/chat/stream/modern",
            "docs": "/docs"
        },
        "implementations": {
            "custom": "Custom LangGraph implementation with MessagesState",
            "modern": "Modern implementation using prebuilt create_react_agent"
        }
    }
