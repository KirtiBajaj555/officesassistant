import asyncio
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from livekit import api
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).parent / '.env')

# Set up logging
logger = logging.getLogger("call-agent-mcp")
logger.setLevel(logging.INFO)

# Configuration
ROOM_NAME = "my-room"
AGENT_NAME = "test-agent"
OUTBOUND_TRUNK_ID = os.getenv("SIP_OUTBOUND_TRUNK_ID")

# Initialize FastMCP server
mcp = FastMCP("Call Agent")

@mcp.tool()
async def make_phone_call(phone_number: str) -> str:
    """
    Initiates a phone call to the specified number using the LiveKit agent.
    
    Args:
        phone_number: The phone number to call (e.g., +1234567890).
    """
    logger.info(f"Received request to call {phone_number}")
    
    if not OUTBOUND_TRUNK_ID or not OUTBOUND_TRUNK_ID.startswith("ST_"):
        error_msg = "SIP_OUTBOUND_TRUNK_ID is not set or invalid"
        logger.error(error_msg)
        return f"Error: {error_msg}"

    lkapi = api.LiveKitAPI()
    
    try:
        # 1. Create agent dispatch
        logger.info(f"Creating dispatch for agent {AGENT_NAME} in room {ROOM_NAME}")
        dispatch = await lkapi.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(
                agent_name=AGENT_NAME, room=ROOM_NAME, metadata=phone_number
            )
        )
        logger.info(f"Created dispatch: {dispatch}")
        
        # 2. Create SIP participant to make the call
        logger.info(f"Dialing {phone_number} to room {ROOM_NAME}")
        
        sip_participant = await lkapi.sip.create_sip_participant(
            api.CreateSIPParticipantRequest(
                room_name=ROOM_NAME,
                sip_trunk_id=OUTBOUND_TRUNK_ID,
                sip_call_to=phone_number,
                participant_identity="phone_user",
            )
        )
        logger.info(f"Created SIP participant: {sip_participant}")
        
        return f"Successfully initiated call to {phone_number}. Dispatch ID: {dispatch.id}, SIP Participant: {sip_participant}"

    except Exception as e:
        logger.error(f"Error making call: {e}")
        return f"Error initiating call: {str(e)}"
    finally:
        await lkapi.aclose()

if __name__ == "__main__":
    mcp.run()
