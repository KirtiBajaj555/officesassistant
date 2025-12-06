import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli, llm
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

    async def summarize(self):
        """Summarize the conversation using the LLM"""
        logger.info("Generating conversation summary...")
        
        # Get chat history
        # The chat_ctx in Agent is iterable and yields messages
        messages = list(self.chat_ctx)
        if not messages:
            logger.info("No messages to summarize")
            return

        # Prepare prompt for summarization
        prompt = "Please summarize the following conversation:\n\n"
        for msg in messages:
            role = msg.role
            content = msg.content
            if content:
                prompt += f"{role}: {content}\n"
        
        prompt += "\nSummary:"

        # Generate summary using the configured LLM
        try:
            # We create a new chat context for the summary generation to avoid messing with the main one
            summary_stream = await self.llm.chat(
                chat_ctx=llm.ChatContext().append(text=prompt, role=llm.ChatRole.USER)
            )
            
            full_summary = ""
            async for chunk in summary_stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_summary += content
            
            print("\n" + "="*50)
            print("CONVERSATION SUMMARY")
            print("="*50)
            print(full_summary)
            print("="*50 + "\n")
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")

async def entrypoint(ctx: JobContext):
    """Main entrypoint for the agent"""
    logger.info(f"🚀 Agent starting in room: {ctx.room.name}")
    
    session = AgentSession()
    agent = SimpleAgent()
    
    await session.start(
        agent=agent,
        room=ctx.room
    )
    
    logger.info("✅ Agent session ended")
    
    # Generate summary after session ends
    await agent.summarize()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))