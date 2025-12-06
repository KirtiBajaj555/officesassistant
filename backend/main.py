# mypy: ignore-errors

import asyncio
import os
from langchain_google_genai import ChatGoogleGenerativeAI # type: ignore
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent # type: ignore
from langchain_mcp_adapters.client import MultiServerMCPClient # type: ignore
from langgraph.checkpoint.memory import MemorySaver # type: ignore
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# Ensure API key is set via environment (load from .env)
if not os.getenv("GOOGLE_API_KEY"):
    raise EnvironmentError("GOOGLE_API_KEY not set in environment. Please add it to .env file.")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    max_output_tokens=512,
)

async def create_agent_for_user(access_token: str, user_id: str):
    """
    Create an agent instance with user-specific credentials.
    
    Args:
        access_token: Google OAuth access token for the user
        user_id: Unique identifier for the user
        
    Returns:
        Configured LangGraph agent
    """
    logger.info(f"Creating agent for user: {user_id}")
    
    # Determine base paths for MCP servers
    # In Docker: /app, Locally: parent of backend directory
    if os.path.exists("/app/gmail"):
        base_path = "/app"
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # MCP client config with user-specific environment variables
    client = MultiServerMCPClient({
        "gmail_sender": {
            "transport": "stdio",
            "command": "uv",
            "args": ["run", f"{base_path}/gmail/server.py"],
            "env": {
                "GOOGLE_ACCESS_TOKEN": access_token,
                "USER_ID": user_id,
                **dict(os.environ)  # Include other env vars
            }
        },
        "calendar_manager": {
            "transport": "stdio",
            "command": "uv",
            "args": ["run", f"{base_path}/calendar/server.py"],
            "env": {
                "GOOGLE_ACCESS_TOKEN": access_token,
                "USER_ID": user_id,
                **dict(os.environ)
            }
        },
        "call_agent": {
            "transport": "stdio",
            "command": "uv",
            "args": ["run", f"{base_path}/thecallagent/server.py"],
            "env": {
                "GOOGLE_ACCESS_TOKEN": access_token,
                "USER_ID": user_id,
                **dict(os.environ)
            }
        }
    })

    tools = await client.get_tools()
    logger.info(f"Loaded {len(tools)} tools for user {user_id}")

    model = llm

    agent = create_react_agent(
        model=model,
        tools=tools,
        checkpointer=MemorySaver()
    )

    return agent

def print_stream_item(item):
    """Print agent stream items with detailed debugging."""
    print(f"\n[DEBUG] Event keys: {list(item.keys())}")
    
    # Handle agent messages
    if "agent" in item:
        messages = item["agent"].get("messages", [])
        print(f"[DEBUG] Agent has {len(messages)} message(s)")
        
        for message in messages:
            # Print message type
            msg_type = getattr(message, '__class__', type(message)).__name__
            print(f"[DEBUG] Message type: {msg_type}")
            
            # Handle content
            content = message.content if hasattr(message, 'content') else message
            
            if isinstance(content, str):
                print(f"Agent > {content}")
            elif isinstance(content, list):
                for part in content:
                    if isinstance(part, str):
                        print(f"Agent > {part}")
                    elif isinstance(part, dict):
                        if "text" in part:
                            print(f"Agent > {part['text']}")
                        elif part.get("type") == "tool_use":
                            print(f"🔧 Using tool: {part.get('name', 'unknown')}")
                            if "input" in part:
                                print(f"   Input: {part['input']}")
                        else:
                            print(f"[DEBUG] Unknown part type: {part}")
            
            # Handle tool calls
            if hasattr(message, 'tool_calls') and message.tool_calls:
                print(f"[DEBUG] Tool calls found: {len(message.tool_calls)}")
                for tool_call in message.tool_calls:
                    print(f"🔧 Calling tool: {tool_call.get('name', 'unknown')}")
                    print(f"   Args: {tool_call.get('args', {})}")
    
    # Handle tool execution results
    elif "tools" in item:
        print(f"[DEBUG] Tool execution results:")
        for msg in item["tools"].get("messages", []):
            if hasattr(msg, 'content'):
                print(f"Tool Result > {msg.content[:200]}...")  # First 200 chars
            else:
                print(f"Tool Result > {msg}")
    
    # Handle any other event types
    else:
        print(f"[DEBUG] Other event: {item}")


async def main():
    """
    Main function for CLI-based testing.
    For production, use api.py instead.
    """
    print("⚠️  Running in CLI mode (for testing only)")
    print("For production, use: uvicorn api:app\n")
    
    # For CLI testing, use a dummy token (will fail with real Google APIs)
    # In production, tokens come from the Flutter app via api.py
    dummy_token = "test_token_for_cli"
    dummy_user_id = "test_user"
    
    agent = await create_agent_for_user(dummy_token, dummy_user_id)

    config = {"configurable": {"thread_id": "1"}}
    print("Agent is ready! Type your command (e.g. 'list my latest emails'):\n")

    while True:
        # Use run_in_executor to avoid blocking the event loop
        user_input = await asyncio.get_running_loop().run_in_executor(None, input, "\nUser > ")
        print(f"[DEBUG] Processing input: '{user_input}'")
        
        async for item in agent.astream(
            {"messages": {"role": "user", "content": user_input}},
            config,
        ):
            print_stream_item(item)
        
        print("[DEBUG] Finished processing input")


if __name__ == "__main__":
    asyncio.run(main())