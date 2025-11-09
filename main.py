# mypy: ignore-errors

import asyncio
import os
from langchain_google_genai import ChatGoogleGenerativeAI # type: ignore

from langchain_mcp_adapters.client import MultiServerMCPClient # type: ignore
from langgraph.checkpoint.memory import InMemorySaver # type: ignore
from langgraph.prebuilt import create_react_agent  # type: ignore

#os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"
# os.environ["GOOGLE_API_KEY"] = "AIzaSyBauKF8LMohkRh7MWTLPDQ4KG4STVcduII"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    max_output_tokens=512,
)

def print_stream_item(item):
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
            elif "text" in c:
                print(f"Agent > {c['text']}")
            elif c["type"] == "tool_use":
                print(f"    using tool: {c['name']}")


async def main():
    # MCP client config
    client = MultiServerMCPClient({
    "email": {  # Gmail MCP
        "transport": "stdio",
        "command": "node",
        "args": ["/home/keshavbajaj/Gmail-MCP-Server/dist/index.js"]
    },
    "playwright": {
        "transport": "stdio",
        "command": "npx",
        "args": ["@playwright/mcp@latest"]
    }
})


    tools = await client.get_tools()
    

    model = llm

    agent = create_react_agent(
        model=model,
        tools=tools,
        checkpointer=InMemorySaver()
    )

    config = {"configurable": {"thread_id": "1"}}
    print("Agent is ready! Type your command (e.g. 'list my latest emails'):\n")

    while True:
        user_input = input("User > ")
        async for item in agent.astream(
            {"messages": {"role": "user", "content": user_input}},
            config,
        ):
            print_stream_item(item)


if __name__ == "__main__":
    asyncio.run(main())