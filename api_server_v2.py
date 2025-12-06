"""
Unified API Server for Office Assistant
Integrates FastAPI with LangChain Agent and MCP Servers
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
import logging
from datetime import datetime
import json
import time

# Import LangChain agent
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from backend.main import create_agent_for_user

# Import calling agent
from thecallagent.make_calls import make_call

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Office Assistant Unified API",
    description="Backend API with LangChain Agent Integration",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    user_id: str
    access_token: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: str

class CallRequest(BaseModel):
    phone_number: str
    context: Optional[str] = None

class CallResponse(BaseModel):
    status: str
    message: str
    call_id: Optional[str] = None

# Agent Pool for caching (reduces latency)
class AgentPool:
    def __init__(self):
        self.agents = {}
        self.last_used = {}
        self.lock = asyncio.Lock()
    
    async def get_agent(self, user_id: str, access_token: str):
        """Get or create agent for user"""
        async with self.lock:
            if user_id in self.agents:
                logger.info(f"Reusing cached agent for user: {user_id}")
                self.last_used[user_id] = time.time()
                return self.agents[user_id]
            
            logger.info(f"Creating new agent for user: {user_id}")
            agent = await create_agent_for_user(access_token, user_id)
            self.agents[user_id] = agent
            self.last_used[user_id] = time.time()
            return agent
    
    async def cleanup_old_agents(self):
        """Remove agents not used in 30 minutes"""
        cutoff = time.time() - 1800  # 30 minutes
        async with self.lock:
            to_remove = [
                uid for uid, last_time in self.last_used.items()
                if last_time < cutoff
            ]
            for uid in to_remove:
                logger.info(f"Removing inactive agent for user: {uid}")
                del self.agents[uid]
                del self.last_used[uid]

# Global agent pool
agent_pool = AgentPool()

# Background task for cleanup
async def cleanup_task():
    """Periodically cleanup old agents"""
    while True:
        await asyncio.sleep(300)  # Every 5 minutes
        await agent_pool.cleanup_old_agents()

@app.on_event("startup")
async def startup_event():
    """Start background tasks"""
    asyncio.create_task(cleanup_task())
    logger.info("✅ Unified API Server started")
    logger.info("📊 Agent pool initialized")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Office Assistant Unified API",
        "version": "2.0.0",
        "features": ["langchain", "mcp", "streaming"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "online",
            "langchain": "available",
            "mcp_gmail": "available",
            "mcp_calendar": "available",
            "mcp_calling": "available"
        },
        "agent_pool": {
            "active_agents": len(agent_pool.agents),
            "cached_users": list(agent_pool.agents.keys())
        }
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint - uses LangChain agent with MCP tools
    """
    try:
        user_message = request.message.strip()
        user_id = request.user_id
        access_token = request.access_token
        
        logger.info(f"Chat request from user {user_id}: {user_message[:50]}...")
        
        # Get or create agent for user
        agent = await agent_pool.get_agent(user_id, access_token)
        
        # Configure agent with thread ID
        config = {"configurable": {"thread_id": user_id}}
        
        # Process message with agent
        response_text = ""
        tool_calls = []
        
        async for chunk in agent.astream(
            {"messages": {"role": "user", "content": user_message}},
            config
        ):
            # Extract agent messages
            if "agent" in chunk:
                for message in chunk["agent"].get("messages", []):
                    if hasattr(message, 'content') and isinstance(message.content, str):
                        response_text += message.content
                    
                    # Track tool calls
                    if hasattr(message, 'tool_calls') and message.tool_calls:
                        for tool_call in message.tool_calls:
                            tool_calls.append({
                                "name": tool_call.get('name', 'unknown'),
                                "args": tool_call.get('args', {})
                            })
            
            # Extract tool results
            elif "tools" in chunk:
                for msg in chunk["tools"].get("messages", []):
                    if hasattr(msg, 'content'):
                        # Tool results are included in final response
                        pass
        
        # If no response, provide default
        if not response_text:
            response_text = "I processed your request. Let me know if you need anything else!"
        
        logger.info(f"Response generated for user {user_id}: {len(response_text)} chars")
        
        return ChatResponse(
            response=response_text,
            metadata={
                "processed_at": datetime.now().isoformat(),
                "tool_calls": tool_calls,
                "agent_cached": user_id in agent_pool.agents
            },
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """
    Streaming chat endpoint - sends responses as they're generated
    """
    async def generate():
        try:
            user_message = request.message.strip()
            user_id = request.user_id
            access_token = request.access_token
            
            logger.info(f"Stream request from user {user_id}: {user_message[:50]}...")
            
            # Get or create agent
            agent = await agent_pool.get_agent(user_id, access_token)
            config = {"configurable": {"thread_id": user_id}}
            
            # Stream chunks
            async for chunk in agent.astream(
                {"messages": {"role": "user", "content": user_message}},
                config
            ):
                # Send agent messages as SSE
                if "agent" in chunk:
                    for message in chunk["agent"].get("messages", []):
                        if hasattr(message, 'content') and isinstance(message.content, str):
                            # Send as Server-Sent Event
                            yield f"data: {json.dumps({'type': 'message', 'content': message.content})}\n\n"
                
                # Send tool call notifications
                if "agent" in chunk:
                    for message in chunk["agent"].get("messages", []):
                        if hasattr(message, 'tool_calls') and message.tool_calls:
                            for tool_call in message.tool_calls:
                                yield f"data: {json.dumps({'type': 'tool_call', 'name': tool_call.get('name')})}\n\n"
            
            # Send completion event
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            
        except Exception as e:
            logger.error(f"Error in stream endpoint: {str(e)}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.post("/api/make-call", response_model=CallResponse)
async def make_call_endpoint(request: CallRequest):
    """
    Endpoint to initiate phone calls using LiveKit
    """
    try:
        phone_number = request.phone_number.strip()
        logger.info(f"Initiating call to: {phone_number}")
        
        # Validate phone number format
        if not phone_number.startswith('+'):
            raise HTTPException(
                status_code=400,
                detail="Phone number must be in international format (e.g., +1234567890)"
            )
        
        # Call the make_call function
        await make_call(phone_number)
        
        return CallResponse(
            status="success",
            message=f"Call initiated to {phone_number}",
            call_id=f"call_{datetime.now().timestamp()}"
        )
        
    except Exception as e:
        logger.error(f"Error making call: {str(e)}")
        return CallResponse(
            status="error",
            message=f"Failed to initiate call: {str(e)}",
            call_id=None
        )

@app.get("/api/agent-status/{user_id}")
async def get_agent_status(user_id: str):
    """Get agent status for a user"""
    return {
        "user_id": user_id,
        "agent_cached": user_id in agent_pool.agents,
        "last_used": agent_pool.last_used.get(user_id),
        "total_cached_agents": len(agent_pool.agents)
    }

@app.delete("/api/agent-cache/{user_id}")
async def clear_agent_cache(user_id: str):
    """Clear cached agent for a user"""
    async with agent_pool.lock:
        if user_id in agent_pool.agents:
            del agent_pool.agents[user_id]
            del agent_pool.last_used[user_id]
            return {"status": "success", "message": f"Agent cache cleared for {user_id}"}
        else:
            return {"status": "not_found", "message": f"No cached agent for {user_id}"}

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Starting Office Assistant Unified API Server...")
    logger.info("📱 Flutter app can connect to: http://localhost:8000")
    logger.info("🤖 LangChain agent with MCP tools enabled")
    logger.info("⚡ Agent caching enabled for reduced latency")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
