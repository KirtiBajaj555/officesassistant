import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import os.path
import asyncio
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import hashlib
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fastmcp import FastMCP

# Define the scopes required for the Gmail API
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.metadata"
]

# Path to your downloaded credentials file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
ATTACHMENTS_DIR = os.path.join(BASE_DIR, "attachments")

# Ensure attachments directory exists
os.makedirs(ATTACHMENTS_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO)
mcp = FastMCP("Gmail Manager")

# Cache for authenticated services
_service_cache: Dict[str, Any] = {}


def _get_token_file(user_email: Optional[str] = None) -> str:
    """Get the token file path for a specific user email."""
    if user_email:
        email_hash = hashlib.md5(user_email.encode()).hexdigest()[:8]
        return os.path.join(BASE_DIR, f"token_{email_hash}.json")
    return os.path.join(BASE_DIR, "token.json")


def get_gmail_service(user_email: Optional[str] = None):
    """Authenticates and returns an authorized Gmail API service instance.
    
    Args:
        user_email: Optional email address for multi-account support.
                   If None, uses the default token.
    """
    # Check for access token from environment (multi-user mode)
    access_token = os.getenv("GOOGLE_ACCESS_TOKEN")
    user_id = os.getenv("USER_ID")
    
    if access_token:
        # Production mode: Use access token from environment
        # In production, Flutter will provide a full OAuth token
        cache_key = user_id or "token_user"
        
        # Return cached service if available
        if cache_key in _service_cache:
            return _service_cache[cache_key]
        
        # For development: If we have a full token.json, use it
        # This happens when we auto-load from token.json in dev mode
        token_file = _get_token_file(user_email)
        if os.path.exists(token_file):
            logging.info(f"Using full credentials from token file for user: {user_id}")
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        else:
            # Production: Create credentials from just the access token
            # Note: This requires the token to be valid and not expired
            creds = Credentials(token=access_token)
        
        # Build the Gmail service
        service = build("gmail", "v1", credentials=creds)
        _service_cache[cache_key] = service
        logging.info(f"Gmail service created for user: {user_id}")
        return service
    
    # Development mode: Use OAuth flow with credentials.json
    cache_key = user_email or "default"
    
    # Return cached service if available
    if cache_key in _service_cache:
        return _service_cache[cache_key]
    
    token_file = _get_token_file(user_email)
    creds = None
    
    # The token.json file stores the user's access and refresh tokens
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # If there are no valid credentials available, initiate the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    
    # Build the Gmail service
    service = build("gmail", "v1", credentials=creds)
    _service_cache[cache_key] = service
    return service


def _parse_email_headers(headers: List[Dict]) -> Dict[str, str]:
    """Parse email headers into a dictionary."""
    result = {}
    for header in headers:
        name = header.get("name", "").lower()
        value = header.get("value", "")
        result[name] = value
    return result


def _format_email_summary(message: Dict) -> str:
    """Format an email message into a readable summary."""
    msg_id = message.get("id", "")
    snippet = message.get("snippet", "")
    
    headers = _parse_email_headers(message.get("payload", {}).get("headers", []))
    subject = headers.get("subject", "(No Subject)")
    from_addr = headers.get("from", "(Unknown)")
    date = headers.get("date", "")
    
    return f"ID: {msg_id}\nFrom: {from_addr}\nSubject: {subject}\nDate: {date}\nSnippet: {snippet}\n"


def _get_email_body(payload: Dict) -> str:
    """Extract the email body from the payload."""
    body = ""
    
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data", "")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                    break
            elif part.get("mimeType") == "text/html" and not body:
                data = part.get("body", {}).get("data", "")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    else:
        data = payload.get("body", {}).get("data", "")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    
    return body


def _create_message(to: str, subject: str, body: str, cc: Optional[str] = None, 
                   bcc: Optional[str] = None, reply_to_id: Optional[str] = None) -> Dict:
    """Create a MIME message."""
    message = MIMEMultipart() if cc or bcc else MIMEText(body)
    
    if isinstance(message, MIMEMultipart):
        message.attach(MIMEText(body, "plain"))
    
    message["to"] = to
    message["subject"] = subject
    
    if cc:
        message["cc"] = cc
    if bcc:
        message["bcc"] = bcc
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    result = {"raw": raw_message}
    if reply_to_id:
        result["threadId"] = reply_to_id
    
    return result


# ============================================================================
# MCP TOOLS
# ============================================================================

@mcp.tool()
def get_user_info(user_email: Optional[str] = None) -> str:
    """Get Gmail user profile information.
    
    Args:
        user_email: Optional email address for multi-account support.
    
    Returns:
        User profile information as a formatted string.
    """
    try:
        service = get_gmail_service(user_email)
        profile = service.users().getProfile(userId="me").execute()
        
        return f"""Gmail User Information:
Email: {profile.get('emailAddress', 'N/A')}
Messages Total: {profile.get('messagesTotal', 0)}
Threads Total: {profile.get('threadsTotal', 0)}
History ID: {profile.get('historyId', 'N/A')}"""
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to get user info. Error: {error}"


def _list_emails_impl(max_results: int = 10, query: Optional[str] = None, 
                      include_spam_trash: bool = False, user_email: Optional[str] = None) -> str:
    """Internal implementation for listing emails."""
    try:
        service = get_gmail_service(user_email)
        
        results = service.users().messages().list(
            userId="me",
            maxResults=max_results,
            q=query,
            includeSpamTrash=include_spam_trash
        ).execute()
        
        messages = results.get("messages", [])
        
        if not messages:
            return "No emails found."
        
        output = [f"Found {len(messages)} email(s):\n"]
        
        for msg in messages:
            msg_detail = service.users().messages().get(
                userId="me", id=msg["id"], format="metadata",
                metadataHeaders=["From", "Subject", "Date"]
            ).execute()
            output.append(_format_email_summary(msg_detail))
            output.append("-" * 80)
        
        return "\n".join(output)
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to list emails. Error: {error}"


@mcp.tool()
def list_emails(max_results: int = 10, query: Optional[str] = None, 
                include_spam_trash: bool = False, user_email: Optional[str] = None) -> str:
    """List emails from Gmail inbox.
    
    Args:
        max_results: Maximum number of emails to return (default: 10).
        query: Optional Gmail search query (e.g., "is:unread", "from:example@gmail.com").
        include_spam_trash: Whether to include spam and trash (default: False).
        user_email: Optional email address for multi-account support.
    
    Returns:
        List of emails as a formatted string.
    """
    return _list_emails_impl(max_results, query, include_spam_trash, user_email)


@mcp.tool()
def search_emails(query: str, max_results: int = 20, user_email: Optional[str] = None) -> str:
    """Search emails using Gmail query syntax.
    
    Args:
        query: Gmail search query (e.g., "is:unread after:2024/01/01", "has:attachment from:example@gmail.com").
        max_results: Maximum number of results (default: 20).
        user_email: Optional email address for multi-account support.
    
    Returns:
        Search results as a formatted string.
    
    Examples:
        - "is:unread" - Find unread emails
        - "from:example@gmail.com" - Find emails from specific sender
        - "has:attachment" - Find emails with attachments
        - "after:2024/01/01 before:2024/12/31" - Find emails in date range
    """
    return _list_emails_impl(max_results=max_results, query=query, user_email=user_email)


@mcp.tool()
def get_email(message_id: str, format: str = "full", user_email: Optional[str] = None) -> str:
    """Get complete email content by ID.
    
    Args:
        message_id: The ID of the email message.
        format: Format of the message ("full", "metadata", "minimal"). Default: "full".
        user_email: Optional email address for multi-account support.
    
    Returns:
        Complete email content as a formatted string.
    """
    try:
        service = get_gmail_service(user_email)
        message = service.users().messages().get(
            userId="me", id=message_id, format=format
        ).execute()
        
        headers = _parse_email_headers(message.get("payload", {}).get("headers", []))
        body = _get_email_body(message.get("payload", {}))
        
        return f"""Email Details:
ID: {message.get('id', '')}
Thread ID: {message.get('threadId', '')}
From: {headers.get('from', 'N/A')}
To: {headers.get('to', 'N/A')}
Subject: {headers.get('subject', '(No Subject)')}
Date: {headers.get('date', 'N/A')}

Body:
{body}
"""
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to get email. Error: {error}"


@mcp.tool()
def get_emails(message_ids: str, user_email: Optional[str] = None) -> str:
    """Get multiple emails at once by their IDs.
    
    Args:
        message_ids: Comma-separated list of message IDs.
        user_email: Optional email address for multi-account support.
    
    Returns:
        Multiple email contents as a formatted string.
    """
    try:
        ids = [mid.strip() for mid in message_ids.split(",")]
        service = get_gmail_service(user_email)
        
        output = []
        for msg_id in ids:
            try:
                message = service.users().messages().get(
                    userId="me", id=msg_id, format="full"
                ).execute()
                
                headers = _parse_email_headers(message.get("payload", {}).get("headers", []))
                body = _get_email_body(message.get("payload", {}))
                
                output.append(f"""
{'='*80}
Email ID: {msg_id}
From: {headers.get('from', 'N/A')}
Subject: {headers.get('subject', '(No Subject)')}
Date: {headers.get('date', 'N/A')}

{body[:500]}{'...' if len(body) > 500 else ''}
""")
            except HttpError as e:
                output.append(f"\nFailed to get email {msg_id}: {e}")
        
        return "\n".join(output)
    except Exception as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to get emails. Error: {error}"


@mcp.tool()
def create_draft(to: str, subject: str, body: str, cc: Optional[str] = None, 
                bcc: Optional[str] = None, user_email: Optional[str] = None) -> str:
    """Create a new draft email.
    
    Args:
        to: Recipient email address.
        subject: Email subject.
        body: Email body text.
        cc: Optional CC recipients (comma-separated).
        bcc: Optional BCC recipients (comma-separated).
        user_email: Optional email address for multi-account support.
    
    Returns:
        Draft ID and confirmation message.
    """
    try:
        service = get_gmail_service(user_email)
        message = _create_message(to, subject, body, cc, bcc)
        
        draft = service.users().drafts().create(
            userId="me",
            body={"message": message}
        ).execute()
        
        draft_id = draft.get("id", "")
        logging.info(f"Draft created successfully! Draft ID: {draft_id}")
        return f"Draft created successfully! Draft ID: {draft_id}"
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to create draft. Error: {error}"


@mcp.tool()
def delete_draft(draft_id: str, user_email: Optional[str] = None) -> str:
    """Delete a draft email.
    
    Args:
        draft_id: The ID of the draft to delete.
        user_email: Optional email address for multi-account support.
    
    Returns:
        Confirmation message.
    """
    try:
        service = get_gmail_service(user_email)
        service.users().drafts().delete(userId="me", id=draft_id).execute()
        
        logging.info(f"Draft {draft_id} deleted successfully!")
        return f"Draft {draft_id} deleted successfully!"
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to delete draft. Error: {error}"


@mcp.tool()
def reply_to_email(message_id: str, body: str, send_immediately: bool = True, 
                  cc: Optional[str] = None, user_email: Optional[str] = None) -> str:
    """Reply to an existing email.
    
    Args:
        message_id: The ID of the email to reply to.
        body: Reply message body.
        send_immediately: If True, send the reply immediately. If False, save as draft.
        cc: Optional CC recipients (comma-separated).
        user_email: Optional email address for multi-account support.
    
    Returns:
        Confirmation message with message/draft ID.
    """
    try:
        service = get_gmail_service(user_email)
        
        # Get the original message
        original = service.users().messages().get(
            userId="me", id=message_id, format="metadata",
            metadataHeaders=["From", "Subject", "To"]
        ).execute()
        
        headers = _parse_email_headers(original.get("payload", {}).get("headers", []))
        original_from = headers.get("from", "")
        original_subject = headers.get("subject", "")
        
        # Extract email address from "Name <email@example.com>" format
        if "<" in original_from:
            to_email = original_from.split("<")[1].split(">")[0]
        else:
            to_email = original_from
        
        # Add "Re: " prefix if not already present
        reply_subject = original_subject if original_subject.startswith("Re:") else f"Re: {original_subject}"
        
        message = _create_message(to_email, reply_subject, body, cc, reply_to_id=message_id)
        
        if send_immediately:
            sent = service.users().messages().send(userId="me", body=message).execute()
            msg_id = sent.get("id", "")
            logging.info(f"Reply sent successfully! Message ID: {msg_id}")
            return f"Reply sent successfully! Message ID: {msg_id}"
        else:
            draft = service.users().drafts().create(
                userId="me",
                body={"message": message}
            ).execute()
            draft_id = draft.get("id", "")
            logging.info(f"Reply saved as draft! Draft ID: {draft_id}")
            return f"Reply saved as draft! Draft ID: {draft_id}"
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to reply to email. Error: {error}"


@mcp.tool()
def save_attachments(message_id: str, output_dir: Optional[str] = None, 
                    user_email: Optional[str] = None) -> str:
    """Save all attachments from an email to local storage.
    
    Args:
        message_id: The ID of the email message.
        output_dir: Optional output directory. Defaults to gmail/attachments/.
        user_email: Optional email address for multi-account support.
    
    Returns:
        List of saved attachment filenames.
    """
    try:
        service = get_gmail_service(user_email)
        message = service.users().messages().get(
            userId="me", id=message_id, format="full"
        ).execute()
        
        save_dir = output_dir or ATTACHMENTS_DIR
        os.makedirs(save_dir, exist_ok=True)
        
        saved_files = []
        
        def process_parts(parts):
            for part in parts:
                if part.get("filename"):
                    attachment_id = part.get("body", {}).get("attachmentId")
                    if attachment_id:
                        attachment = service.users().messages().attachments().get(
                            userId="me", messageId=message_id, id=attachment_id
                        ).execute()
                        
                        file_data = base64.urlsafe_b64decode(attachment["data"])
                        filename = part["filename"]
                        filepath = os.path.join(save_dir, filename)
                        
                        with open(filepath, "wb") as f:
                            f.write(file_data)
                        
                        saved_files.append(filename)
                        logging.info(f"Saved attachment: {filename}")
                
                # Recursively process nested parts
                if "parts" in part:
                    process_parts(part["parts"])
        
        payload = message.get("payload", {})
        if "parts" in payload:
            process_parts(payload["parts"])
        
        if not saved_files:
            return "No attachments found in this email."
        
        return f"Saved {len(saved_files)} attachment(s) to {save_dir}:\n" + "\n".join(f"- {f}" for f in saved_files)
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to save attachments. Error: {error}"


@mcp.tool()
def send_email(to: str, subject: str, body: str, cc: Optional[str] = None, 
              bcc: Optional[str] = None, user_email: Optional[str] = None) -> str:
    """Send an email with optional CC and BCC.
    
    Args:
        to: Recipient email address.
        subject: Email subject.
        body: Email body text.
        cc: Optional CC recipients (comma-separated).
        bcc: Optional BCC recipients (comma-separated).
        user_email: Optional email address for multi-account support.
    
    Returns:
        Message ID or error status string.
    """
    try:
        service = get_gmail_service(user_email)
        message = _create_message(to, subject, body, cc, bcc)
        
        sent_message = service.users().messages().send(userId="me", body=message).execute()
        msg_id = sent_message.get("id", "")
        logging.info(f"Email sent successfully! Message ID: {msg_id}")
        return f"Email sent successfully! Message ID: {msg_id}"
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to send email. Error: {error}"


# Keep the old function name for backward compatibility
@mcp.tool()
def send_automated_email(to_email: str, subject: str, body: str) -> str:
    """Legacy function - use send_email instead.
    
    Sends an automated email to a specified recipient.
    
    Args:
        to_email: The recipient's email address.
        subject: The subject line of the email.
        body: The plain text body of the email.
    
    Returns:
        A message ID or error status string.
    """
    return send_email(to_email, subject, body)


if __name__ == "__main__":
    # Check if token exists, if not, run OAuth flow
    if not os.path.exists(_get_token_file()):
        logging.info("Token file not found. Starting OAuth flow...")
        try:
            get_gmail_service()
            logging.info("Authentication successful. token.json created.")
        except Exception as e:
            logging.error(f"Error during OAuth flow: {e}")
            exit(1)
    
    logging.info("Starting Gmail MCP Server...")
    asyncio.run(mcp.run_async(transport="stdio"))