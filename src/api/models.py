"""
Pydantic models for the API
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    session_id: str
    tools_used: List[str]
    metadata: Dict[str, Any]
    timestamp: datetime

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: datetime
    version: str

class StreamChunk(BaseModel):
    """Streaming response chunk model."""
    chunk_type: str  # "agent", "tools", "end"
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
