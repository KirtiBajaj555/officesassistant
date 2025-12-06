import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List tools
            tools = await session.list_tools()
            print("Connected to server. Available tools:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            # Make a call
            print(f"Calling +917774931749...")
            result = await session.call_tool("make_phone_call", arguments={"phone_number": "+917774931749"})
            print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(run())
