"""
Quick test for check_availability function
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

async def test_availability():
    """Test the check_availability function"""
    
    client = MultiServerMCPClient({
        "calendar_manager": {
            "transport": "stdio",
            "command": "uv",
            "args": ["run", "/home/keshavbajaj/officeagent/calendar/server.py"]
        }
    })
    
    tools = await client.get_tools()
    print(f"\n{'='*80}")
    print(f"Testing check_availability function")
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
    
    config = {"configurable": {"thread_id": "availability_test"}}
    
    # Calculate tomorrow's date range
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")
    
    test_command = f"Am I free tomorrow ({tomorrow_str}) between 9am and 5pm?"
    
    print(f"Command: {test_command}\n")
    print(f"{'-'*80}\n")
    
    async for item in agent.astream(
        {"messages": {"role": "user", "content": test_command}},
        config,
    ):
        if "agent" in item:
            for message in item["agent"].get("messages", []):
                content = message.content if hasattr(message, 'content') else message
                if isinstance(content, str):
                    print(f"✓ {content}")
                elif isinstance(content, list):
                    for part in content:
                        if isinstance(part, str):
                            print(f"✓ {part}")
                        elif isinstance(part, dict) and "text" in part:
                            print(f"✓ {part['text']}")
    
    print(f"\n{'-'*80}")
    print(f"\n✅ Availability check completed!")
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    asyncio.run(test_availability())
