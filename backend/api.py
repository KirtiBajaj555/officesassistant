# mypy: ignore-errors

"""
Production-ready API with proper OAuth token handling.
Supports both development (token.json) and production (OAuth credentials from Flutter).
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import logging
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Office Agent API",
    description="Multi-user AI assistant for office automation",
    version="1.0.0"
)

# CORS Configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    user_id: str
    # Production: OAuth credentials from Flutter
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_uri: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str

def get_dev_token():
    """
    Development mode: Read token from token.json.
    Returns the full token data for proper OAuth.
    """
    # Try Docker path first (/app/gmail/token.json)
    token_path = Path("/app/gmail/token.json")
    if not token_path.exists():
        # Fallback to relative path for local development
        token_path = Path(__file__).parent.parent / "gmail" / "token.json"
    
    if token_path.exists():
        with open(token_path) as f:
            return json.load(f)
    return None

def save_user_credentials(user_id: str, token_data: dict):
    """
    Save user's OAuth credentials to a JSON file.
    In production, you'd save this to a database instead.
    """
    creds_dir = Path(__file__).parent / "user_credentials"
    creds_dir.mkdir(exist_ok=True)
    
    creds_file = creds_dir / f"{user_id}.json"
    with open(creds_file, "w") as f:
        json.dump(token_data, f)
    
    logger.info(f"Saved credentials for user: {user_id}")

# Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development")
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    authorization: str = Header(None)
):
    """
    Main chat endpoint. Accepts user message and OAuth credentials.
    
    DEVELOPMENT mode: Auto-loads from token.json if no credentials provided
    PRODUCTION mode: Requires OAuth credentials from Flutter
    """
    try:
        # Determine token source
        token_data = None
        
        # Priority 1: OAuth credentials in request body (Production)
        if request.access_token:
            logger.info("Using OAuth credentials from request body")
            token_data = {
                "token": request.access_token,
                "refresh_token": request.refresh_token,
                "token_uri": request.token_uri or "https://oauth2.googleapis.com/token",
                "client_id": request.client_id,
                "client_secret": request.client_secret,
                "scopes": [
                    "https://www.googleapis.com/auth/gmail.modify",
                    "https://www.googleapis.com/auth/calendar"
                ]
            }
            # Save for future requests (in production, save to database)
            save_user_credentials(request.user_id, token_data)
        
        # Priority 2: Authorization header (Production - access token only)
        elif authorization and authorization.startswith("Bearer "):
            access_token = authorization.replace("Bearer ", "")
            logger.info("Using access token from Authorization header")
            
            # Try to load saved credentials for this user
            creds_file = Path(__file__).parent / "user_credentials" / f"{request.user_id}.json"
            if creds_file.exists():
                with open(creds_file) as f:
                    token_data = json.load(f)
                    token_data["token"] = access_token  # Update with fresh token
            else:
                # No saved credentials - use access token only (may fail)
                token_data = {"token": access_token}
        
        # Priority 3: Development mode - auto-load from token.json
        else:
            if os.getenv("ENVIRONMENT") == "production":
                raise HTTPException(
                    status_code=401,
                    detail="Missing OAuth credentials. Please provide access_token or Authorization header."
                )
            
            logger.info("Development mode: Loading from token.json")
            token_data = get_dev_token()
            if not token_data:
                raise HTTPException(
                    status_code=401,
                    detail="No token found. Run 'cd gmail && uv run server.py' to authenticate."
                )
        
        # Import here to avoid circular imports
        from main import create_agent_for_user
        
        logger.info(f"Processing chat request for user: {request.user_id}")
        
        # Create agent instance with user's credentials
        # Pass the access token to the agent
        agent = await create_agent_for_user(
            access_token=token_data.get("token"),
            user_id=request.user_id
        )
        
        # Process message
        config = {"configurable": {"thread_id": request.user_id}}
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": request.message}]},
            config
        )
        
        # Extract response - handle different content formats
        response_content = "No response"
        if result.get("messages"):
            last_message = result["messages"][-1]
            content = last_message.content if hasattr(last_message, 'content') else last_message
            
            # Content can be a string or a list of content blocks
            if isinstance(content, str):
                response_content = content
            elif isinstance(content, list):
                # Extract text from content blocks
                text_parts = []
                for block in content:
                    if isinstance(block, dict) and block.get('type') == 'text':
                        text_parts.append(block.get('text', ''))
                    elif isinstance(block, str):
                        text_parts.append(block)
                response_content = '\n'.join(text_parts) if text_parts else "No text response"
            else:
                response_content = str(content)
        
        logger.info(f"Successfully processed request for user: {request.user_id}")
        
        return ChatResponse(
            response=response_content,
            session_id=request.user_id
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Office Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "mode": os.getenv("ENVIRONMENT", "development")
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
