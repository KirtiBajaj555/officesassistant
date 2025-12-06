"""
Quick test to create a visible event in Google Calendar
"""

import asyncio
import os
from datetime import datetime, timedelta
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

async def quick_test():
    """Create a test event that should be visible in Google Calendar"""
    
    client = MultiServerMCPClient({
        "calendar_manager": {
            "transport": "stdio",
            "command": "uv",
            "args": ["run", "/home/keshavbajaj/officeagent/calendar/server.py"]
        }
    })
    
    tools = await client.get_tools()
    print(f"\n{'='*80}")
    print(f"Quick Calendar Test - Creating Visible Event")
    print(f"{'='*80}\n")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7,
        max_output_tokens=512,
    )
    
    agent = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=MemorySaver()
    )
    
    config = {"configurable": {"thread_id": "quick_test"}}
    
    # Calculate tomorrow's date and time
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")
    
    test_command = f"Create an event called 'Calendar Test Event' on {tomorrow_str} at 2:00 PM for 1 hour with description 'This is a test event to verify calendar integration'"
    
    print(f"Command: {test_command}\n")
    print(f"{'-'*80}\n")
    
    async for item in agent.astream(
        {"messages": {"role": "user", "content": test_command}},
        config,
    ):
        if "agent" in item:
            content = [
                part
                for message in item["agent"]["messages"]
                for part in (
                    message.content
                    if isinstance(message.content, list)
                    else [message.content]
                )
            ]
            for c in content:
                if isinstance(c, str):
                    print(f"✓ {c}")
                elif isinstance(c, dict):
                    if "text" in c:
                        print(f"✓ {c['text']}")
                    elif c.get("type") == "tool_use":
                        print(f"  → Using tool: {c['name']}")
    
    print(f"\n{'-'*80}")
    print(f"\n✅ Test completed! Check your Google Calendar for the event.")
    print(f"   Event should appear on {tomorrow_str} at 2:00 PM IST")
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    asyncio.run(quick_test())
