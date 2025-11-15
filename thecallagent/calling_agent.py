import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import silero, deepgram, google

# Load environment variables
load_dotenv()

logger = logging.getLogger("calling-agent")
logger.setLevel(logging.INFO)

class SimpleAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""
                You are calling someone on the phone. Your goal is to know if they prefer
                chocolate or vanilla ice cream. That's the only question you should ask, and
                you should get right to the point. Say something like "Hello, I'm calling to
                ask you a question about ice cream. Do you prefer chocolate or vanilla?"
                Keep the conversation brief and polite. Once they answer, thank them and end the call.
            """,
            stt=deepgram.STT(model="nova-2"),
            llm=google.LLM(model="gemini-2.5-flash"),
            # Fixed: Use model parameter instead of voice
            tts=deepgram.TTS(model="aura-asteria-en"),
            vad=silero.VAD.load(),
        )

    async def on_enter(self):
        """Called when agent enters the session - generates initial greeting"""
        logger.info("Agent entering session, generating initial greeting...")
        self.session.generate_reply()

async def entrypoint(ctx: JobContext):
    """Main entrypoint for the agent"""
    logger.info(f"🚀 Agent starting in room: {ctx.room.name}")
    
    session = AgentSession()
    await session.start(
        agent=SimpleAgent(),
        room=ctx.room
    )
    
    logger.info("✅ Agent session started successfully")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))