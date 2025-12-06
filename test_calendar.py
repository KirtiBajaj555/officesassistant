"""
Test script for Calendar MCP Server
This script tests all calendar tools through the MCP client
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

# Ensure API key is set
if not os.getenv("GOOGLE_API_KEY"):
    raise EnvironmentError("GOOGLE_API_KEY not set in environment. Please add it to .env file.")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    max_output_tokens=512,
)


async def test_calendar_tools():
    """Test all calendar MCP tools"""
    
    # Initialize MCP client with calendar server
    client = MultiServerMCPClient({
        "calendar_manager": {
            "transport": "stdio",
            "command": "uv",
            "args": ["run", "/home/keshavbajaj/officeagent/calendar/server.py"]
        }
    })
    
    # Get available tools
    tools = await client.get_tools()
    print(f"\n{'='*80}")
    print(f"Loaded {len(tools)} calendar tools from MCP server:")
    print(f"{'='*80}")
    for t in tools:
        print(f" ✓ {t.name}")
    print(f"{'='*80}\n")
    
    # Create agent with tools
    agent = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=MemorySaver()
    )
    
    config = {"configurable": {"thread_id": "test_calendar"}}
    
    # Test commands
    test_commands = [
        # Basic calendar operations
        {
            "name": "List Calendars",
            "command": "List all my calendars"
        },
        {
            "name": "Get Primary Calendar Details",
            "command": "Get details about my primary calendar"
        },
        
        # Event listing and searching
        {
            "name": "List Upcoming Events",
            "command": "Show me my next 5 upcoming events"
        },
        {
            "name": "List Events This Week",
            "command": "What events do I have this week?"
        },
        
        # Create event
        {
            "name": "Create Simple Event",
            "command": f"Create an event called 'Test Meeting' tomorrow at 2pm for 1 hour"
        },
        {
            "name": "Quick Add Event",
            "command": "Quick add: Team standup tomorrow at 10am"
        },
        
        # Search events
        {
            "name": "Search Events",
            "command": "Search for events with 'meeting' in the title"
        },
        
        # Check availability
        {
            "name": "Check Availability",
            "command": f"Am I free tomorrow between 9am and 5pm?"
        },
    ]
    
    # Run each test command
    for i, test in enumerate(test_commands, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}/{len(test_commands)}: {test['name']}")
        print(f"{'='*80}")
        print(f"Command: {test['command']}")
        print(f"{'-'*80}")
        
        try:
            async for item in agent.astream(
                {"messages": {"role": "user", "content": test['command']}},
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
                            print(f"Response: {c}")
                        elif isinstance(c, dict):
                            if "text" in c:
                                print(f"Response: {c['text']}")
                            elif c.get("type") == "tool_use":
                                print(f"  → Using tool: {c['name']}")
            
            print(f"✓ Test completed successfully")
            
        except Exception as e:
            print(f"✗ Test failed with error: {e}")
        
        # Small delay between tests
        await asyncio.sleep(1)
    
    print(f"\n{'='*80}")
    print(f"ALL TESTS COMPLETED")
    print(f"{'='*80}\n")


async def interactive_mode():
    """Interactive mode to test calendar commands manually"""
    
    client = MultiServerMCPClient({
        "calendar_manager": {
            "transport": "stdio",
            "command": "uv",
            "args": ["run", "/home/keshavbajaj/officeagent/calendar/server.py"]
        }
    })
    
    tools = await client.get_tools()
    print(f"\n{'='*80}")
    print(f"Calendar MCP Server - Interactive Mode")
    print(f"{'='*80}")
    print(f"Loaded {len(tools)} tools:")
    for t in tools:
        print(f" ✓ {t.name}")
    print(f"{'='*80}\n")
    
    agent = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=MemorySaver()
    )
    
    config = {"configurable": {"thread_id": "interactive_calendar"}}
    
    print("Example commands you can try:")
    print("  - List all my calendars")
    print("  - Show me my events for today")
    print("  - Create an event called 'Lunch' tomorrow at 12pm")
    print("  - Am I free tomorrow afternoon?")
    print("  - Search for events about 'meeting'")
    print("\nType 'quit' or 'exit' to stop.\n")
    
    while True:
        user_input = await asyncio.get_running_loop().run_in_executor(
            None, input, "\nYou > "
        )
        
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
        
        print(f"{'-'*80}")
        
        async for item in agent.astream(
            {"messages": {"role": "user", "content": user_input}},
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
                        print(f"Agent > {c}")
                    elif isinstance(c, dict):
                        if "text" in c:
                            print(f"Agent > {c['text']}")
                        elif c.get("type") == "tool_use":
                            print(f"  → Using tool: {c['name']}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        print("Starting interactive mode...")
        asyncio.run(interactive_mode())
    else:
        print("Running automated tests...")
        print("(Use --interactive flag for interactive mode)")
        asyncio.run(test_calendar_tools())
