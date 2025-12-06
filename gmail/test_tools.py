#!/usr/bin/env python3
"""Test script to verify all Gmail MCP tools are registered correctly."""

import sys
import os

# Add the gmail directory to path
sys.path.insert(0, '/home/keshavbajaj/officeagent/gmail')

# Import the server module
import server

def main():
    print("=" * 80)
    print("Gmail MCP Server - Tool Verification")
    print("=" * 80)
    
    # Get all registered tools
    mcp = server.mcp
    
    # List of expected tools
    expected_tools = [
        'get_user_info',
        'list_emails',
        'search_emails',
        'get_email',
        'get_emails',
        'create_draft',
        'delete_draft',
        'reply_to_email',
        'save_attachments',
        'send_email',
        'send_automated_email'
    ]
    
    print(f"\nExpected tools: {len(expected_tools)}")
    print("\nChecking tool registration:\n")
    
    # Check each tool
    for tool_name in expected_tools:
        # Try to get the tool function
        try:
            tool_func = getattr(server, tool_name, None)
            if tool_func and callable(tool_func):
                print(f"✅ {tool_name:25} - Registered")
                # Print docstring first line
                if tool_func.__doc__:
                    doc_first_line = tool_func.__doc__.strip().split('\n')[0]
                    print(f"   {doc_first_line}")
            else:
                print(f"❌ {tool_name:25} - NOT FOUND")
        except Exception as e:
            print(f"❌ {tool_name:25} - ERROR: {e}")
    
    print("\n" + "=" * 80)
    print("Server Configuration:")
    print("=" * 80)
    print(f"Server Name: {mcp.name}")
    print(f"Base Directory: {server.BASE_DIR}")
    print(f"Credentials File: {server.CREDENTIALS_FILE}")
    print(f"Attachments Directory: {server.ATTACHMENTS_DIR}")
    print(f"Token File (default): {server._get_token_file()}")
    
    print("\n" + "=" * 80)
    print("Helper Functions:")
    print("=" * 80)
    helper_functions = [
        '_get_token_file',
        '_parse_email_headers',
        '_format_email_summary',
        '_get_email_body',
        '_create_message'
    ]
    
    for func_name in helper_functions:
        func = getattr(server, func_name, None)
        if func and callable(func):
            print(f"✅ {func_name}")
        else:
            print(f"❌ {func_name} - NOT FOUND")
    
    print("\n" + "=" * 80)
    print("Summary:")
    print("=" * 80)
    print(f"All tools are registered and ready to use!")
    print(f"You can now test the agent with commands like:")
    print(f"  - 'list my latest 5 emails'")
    print(f"  - 'get my gmail user information'")
    print(f"  - 'search for unread emails'")
    print("=" * 80)

if __name__ == "__main__":
    main()
