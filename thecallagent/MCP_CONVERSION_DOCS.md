# Call Agent MCP Server Conversion Documentation

## 1. Logic and Process

The goal is to convert the existing `make_calls.py` script into a Model Context Protocol (MCP) server. This allows AI agents (like Claude or a custom agent) to discover and use the "make call" functionality as a tool.

### Current Architecture
- **`calling_agent.py`**: This is the LiveKit worker. It connects to a room and handles the voice conversation logic (STT -> LLM -> TTS). It waits for a job (dispatch) to start.
- **`make_calls.py`**: This script initiates the process. It:
    1. Creates a "dispatch" (a job request) for the `calling_agent`.
    2. Creates a SIP participant (the phone call) and invites them to the room.

### MCP Server Architecture
We will wrap the logic from `make_calls.py` into an MCP server.

- **`server.py`**: The new MCP server.
    - It will expose a tool named `make_phone_call`.
    - This tool will accept a `phone_number` argument.
    - When called, it will execute the same logic as `make_calls.py`: create a dispatch and a SIP participant.

### The Process
1.  **Define the Tool**: We define a function `make_phone_call(phone_number: str)` and decorate it with `@mcp.tool()`.
2.  **Environment Setup**: The server needs access to the same environment variables (`LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `SIP_OUTBOUND_TRUNK_ID`).
3.  **Execution**: The MCP server runs as a standalone process. Clients connect to it (via stdio) and can request to call the tool.

## 2. Implementation Details

We will use the `mcp` python package to create the server. We will use `livekit-api` to interact with LiveKit.

### Key Components
- **`FastMCP`**: A high-level API to quickly build MCP servers.
- **`LiveKitAPI`**: Used to create the dispatch and SIP participant.

## 3. Execution

### Prerequisites
- Python 3.10+
- `uv` (recommended) or `pip`
- Environment variables set in `.env` file:
    - `LIVEKIT_URL`
    - `LIVEKIT_API_KEY`
    - `LIVEKIT_API_SECRET`
    - `SIP_OUTBOUND_TRUNK_ID`

### Running the Server and Agent

You need to run **two** processes:
1. The **MCP Server** (handles the "make call" tool).
2. The **Agent Worker** (handles the voice conversation).

**Terminal 1: Run the MCP Server**
```bash
uv run server.py
```

**Terminal 2: Run the Agent Worker**
```bash
uv run calling_agent.py
```
*Note: The agent will print a summary of the conversation to this terminal after the call ends.*

### Connecting with an MCP Client

To use this server with an MCP client (like Claude Desktop or another agent), configure it to run the server script.

**Example Configuration (Claude Desktop):**

```json
{
  "mcpServers": {
    "call-agent": {
      "command": "uv",
      "args": [
        "run",
        "/absolute/path/to/officeagent/thecallagent/server.py"
      ],
      "env": {
        "SIP_OUTBOUND_TRUNK_ID": "ST_..."
      }
    }
  }
}
```

### Testing

You can use the provided `test_mcp_client.py` to verify the server is running and exposing the tools correctly:

```bash
uv run test_mcp_client.py
```
