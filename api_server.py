"""
FastAPI Backend for Office Assistant Flutter App
Connects Flutter UI with Python backend services
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
import logging
from datetime import datetime

# Import your existing calling agent functionality
from thecallagent.make_calls import make_call

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Office Assistant API",
    description="Backend API for Office Assistant Flutter App",
    version="1.0.0"
)

# Add CORS middleware to allow Flutter app to connect
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

# In-memory conversation history (use database in production)
conversation_history = []

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Office Assistant API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint - processes user messages and returns AI responses
    """
    try:
        user_message = request.message.strip()
        logger.info(f"Received chat message: {user_message}")
        
        # Store message in history
        conversation_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Process the message and generate response
        response_text = await process_message(user_message)
        
        # Store assistant response
        conversation_history.append({
            "role": "assistant",
            "content": response_text,
            "timestamp": datetime.now().isoformat()
        })
        
        return ChatResponse(
            response=response_text,
            metadata={
                "processed_at": datetime.now().isoformat(),
                "message_length": len(response_text)
            },
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_message(message: str) -> str:
    """
    Process user message and generate appropriate response
    This is where you integrate your AI/LLM logic
    """
    message_lower = message.lower()
    
    # Check for phone call requests
    if "call" in message_lower or "phone" in message_lower:
        return """📞 I can help you make a phone call! 

To initiate a call, please provide the phone number in international format (e.g., +1234567890).

You can say something like:
• "Call +1234567890"
• "Make a call to +9876543210"

Or use the attachment button to access the phone dialer directly."""
    
    # Check for email requests
    elif "email" in message_lower or "mail" in message_lower:
        return """📧 I can assist with email management!

I can help you:
• Read your latest emails
• Send new emails
• Search for specific emails
• Organize your inbox
• Set up email filters

What would you like to do with emails?"""
    
    # Check for calendar/scheduling
    elif "calendar" in message_lower or "meeting" in message_lower or "schedule" in message_lower:
        return """📅 Let me help you with calendar management!

I can assist with:
• Viewing your schedule
• Creating new meetings
• Sending meeting invites
• Checking availability
• Setting reminders

What would you like to schedule?"""
    
    # Check for document/file management
    elif "document" in message_lower or "file" in message_lower:
        return """📄 I can help with document management!

Available actions:
• Open and read documents
• Create new documents
• Search for files
• Organize folders
• Share documents

What document task can I help with?"""
    
    # Check for data analysis
    elif "data" in message_lower or "analyze" in message_lower or "report" in message_lower:
        return """📊 I can assist with data analysis!

I can help you:
• Analyze datasets
• Generate reports
• Create visualizations
• Extract insights
• Process spreadsheets

What data would you like to analyze?"""
    
    # Default helpful response
    else:
        return f"""✨ I'm your Office Assistant! I understand you said: "{message}"

I can help you with many tasks:

📞 **Communications**
• Make phone calls
• Manage emails
• Send messages

📅 **Scheduling**
• Calendar management
• Meeting scheduling
• Reminders

📊 **Productivity**
• Document handling
• Data analysis
• Task management

🔍 **Information**
• Quick searches
• Data lookup
• Knowledge queries

What would you like me to help you with?"""

@app.post("/make-call", response_model=CallResponse)
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
        
        # Call your existing make_call function
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

@app.get("/conversation-history")
async def get_conversation_history():
    """
    Retrieve conversation history
    """
    return {
        "history": conversation_history,
        "count": len(conversation_history)
    }

@app.delete("/conversation-history")
async def clear_conversation_history():
    """
    Clear conversation history
    """
    conversation_history.clear()
    return {"status": "success", "message": "Conversation history cleared"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "online",
            "calling": "available",
            "chat": "available"
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Office Assistant API Server...")
    logger.info("Flutter app can connect to: http://localhost:8000")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

