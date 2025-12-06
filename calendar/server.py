import os
import os.path
import asyncio
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import hashlib
from dateutil import parser as date_parser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fastmcp import FastMCP

# Define the scopes required for the Calendar API
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events"
]

# Path to your downloaded credentials file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")

logging.basicConfig(level=logging.INFO)
mcp = FastMCP("Calendar Manager")

# Cache for authenticated services
_service_cache: Dict[str, Any] = {}


def _get_token_file(user_email: Optional[str] = None) -> str:
    """Get the token file path for a specific user email."""
    if user_email:
        email_hash = hashlib.md5(user_email.encode()).hexdigest()[:8]
        return os.path.join(BASE_DIR, f"token_{email_hash}.json")
    return os.path.join(BASE_DIR, "token.json")


def get_calendar_service(user_email: Optional[str] = None):
    """Authenticates and returns an authorized Calendar API service instance.
    
    Args:
        user_email: Optional email address for multi-account support.
    """
    # Check for access token from environment (multi-user mode)
    access_token = os.getenv("GOOGLE_ACCESS_TOKEN")
    user_id = os.getenv("USER_ID")
    
    if access_token:
        # Production mode: Use access token from environment
        cache_key = user_id or "token_user"
        
        if cache_key in _service_cache:
            return _service_cache[cache_key]
        
        # Create credentials from access token
        creds = Credentials(token=access_token)
        
        # Build the Calendar service
        service = build("calendar", "v3", credentials=creds)
        _service_cache[cache_key] = service
        logging.info(f"Calendar service created for user: {user_id}")
        return service
    
    # Development mode: Use OAuth flow with credentials.json
    cache_key = user_email or "default"
    
    if cache_key in _service_cache:
        return _service_cache[cache_key]
    
    token_file = _get_token_file(user_email)
    creds = None
    
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    
    service = build("calendar", "v3", credentials=creds)
    _service_cache[cache_key] = service
    return service


def _parse_datetime(dt_string: str) -> str:
    """Parse various datetime formats and return ISO format."""
    try:
        # Handle special keywords
        dt_string_lower = dt_string.lower().strip()
        
        if dt_string_lower == "now":
            dt = datetime.utcnow()
        elif dt_string_lower == "today":
            dt = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        elif dt_string_lower == "tomorrow":
            dt = (datetime.utcnow() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            # Handle compound expressions like "tomorrow at 12pm", "tomorrow afternoon"
            if "tomorrow" in dt_string_lower:
                # Get tomorrow's date
                tomorrow = datetime.utcnow() + timedelta(days=1)
                
                # Try to extract time from the string
                # Remove "tomorrow" and "at" to get just the time part
                time_part = dt_string_lower.replace("tomorrow", "").replace("at", "").strip()
                
                if time_part:
                    # Parse just the time part
                    try:
                        time_dt = date_parser.parse(time_part, fuzzy=True)
                        # Combine tomorrow's date with the parsed time
                        dt = tomorrow.replace(
                            hour=time_dt.hour,
                            minute=time_dt.minute,
                            second=0,
                            microsecond=0
                        )
                    except:
                        # If time parsing fails, use tomorrow at midnight
                        dt = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
                else:
                    dt = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                # Try to parse the datetime string with fuzzy parsing
                dt = date_parser.parse(dt_string, fuzzy=True)
            
            # If the parsed date is in the past and the string contains "tomorrow", add a day
            if "tomorrow" in dt_string_lower and dt < datetime.utcnow():
                dt = dt + timedelta(days=1)
        
        return dt.isoformat()
    except Exception as e:
        logging.error(f"Failed to parse datetime '{dt_string}': {e}")
        # Return current time as fallback
        return datetime.utcnow().isoformat()


def _format_event(event: Dict) -> str:
    """Format an event for display."""
    event_id = event.get("id", "")
    summary = event.get("summary", "(No Title)")
    start = event.get("start", {}).get("dateTime") or event.get("start", {}).get("date", "")
    end = event.get("end", {}).get("dateTime") or event.get("end", {}).get("date", "")
    location = event.get("location", "")
    description = event.get("description", "")
    attendees = event.get("attendees", [])
    
    output = [
        f"ID: {event_id}",
        f"Summary: {summary}",
        f"Start: {start}",
        f"End: {end}"
    ]
    
    if location:
        output.append(f"Location: {location}")
    if description:
        output.append(f"Description: {description[:100]}{'...' if len(description) > 100 else ''}")
    if attendees:
        attendee_list = ", ".join([a.get("email", "") for a in attendees[:3]])
        if len(attendees) > 3:
            attendee_list += f" (+{len(attendees) - 3} more)"
        output.append(f"Attendees: {attendee_list}")
    
    return "\n".join(output)


def _create_event_body(summary: str, start: str, end: str, description: Optional[str] = None,
                      location: Optional[str] = None, attendees: Optional[str] = None,
                      reminders: Optional[int] = None) -> Dict:
    """Create an event body for API requests."""
    # Parse datetime strings
    start_dt = _parse_datetime(start)
    end_dt = _parse_datetime(end)
    
    # Use Asia/Kolkata timezone instead of UTC
    event = {
        "summary": summary,
        "start": {"dateTime": start_dt, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_dt, "timeZone": "Asia/Kolkata"}
    }
    
    if description:
        event["description"] = description
    if location:
        event["location"] = location
    if attendees:
        # Parse comma-separated attendees
        event["attendees"] = [{"email": email.strip()} for email in attendees.split(",")]
    if reminders:
        event["reminders"] = {
            "useDefault": False,
            "overrides": [{"method": "popup", "minutes": reminders}]
        }
    
    return event


# ============================================================================
# MCP TOOLS
# ============================================================================

@mcp.tool()
def list_calendars(user_email: Optional[str] = None) -> str:
    """List all calendars for the authenticated user.
    
    Args:
        user_email: Optional email address for multi-account support.
    
    Returns:
        List of calendars as a formatted string.
    """
    try:
        service = get_calendar_service(user_email)
        calendars = service.calendarList().list().execute()
        
        items = calendars.get("items", [])
        if not items:
            return "No calendars found."
        
        output = [f"Found {len(items)} calendar(s):\n"]
        for cal in items:
            cal_id = cal.get("id", "")
            summary = cal.get("summary", "")
            primary = " (PRIMARY)" if cal.get("primary", False) else ""
            access_role = cal.get("accessRole", "")
            output.append(f"- {summary}{primary}")
            output.append(f"  ID: {cal_id}")
            output.append(f"  Access: {access_role}\n")
        
        return "\n".join(output)
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to list calendars. Error: {error}"


@mcp.tool()
def get_calendar(calendar_id: str = "primary", user_email: Optional[str] = None) -> str:
    """Get details about a specific calendar.
    
    Args:
        calendar_id: Calendar ID (default: "primary").
        user_email: Optional email address for multi-account support.
    
    Returns:
        Calendar details as a formatted string.
    """
    try:
        service = get_calendar_service(user_email)
        calendar = service.calendars().get(calendarId=calendar_id).execute()
        
        return f"""Calendar Details:
ID: {calendar.get('id', '')}
Summary: {calendar.get('summary', '')}
Description: {calendar.get('description', 'N/A')}
Time Zone: {calendar.get('timeZone', 'N/A')}
Location: {calendar.get('location', 'N/A')}"""
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to get calendar. Error: {error}"


@mcp.tool()
def create_event(summary: str, start: str, end: str, calendar_id: str = "primary",
                description: Optional[str] = None, location: Optional[str] = None,
                attendees: Optional[str] = None, reminders: Optional[int] = None,
                user_email: Optional[str] = None) -> str:
    """Create a new calendar event.
    
    Args:
        summary: Event title/summary.
        start: Start time (ISO format or natural language like "2024-12-01T10:00:00").
        end: End time (ISO format or natural language).
        calendar_id: Calendar ID (default: "primary").
        description: Optional event description.
        location: Optional event location.
        attendees: Optional comma-separated list of attendee emails.
        reminders: Optional reminder time in minutes before event.
        user_email: Optional email address for multi-account support.
    
    Returns:
        Event ID and confirmation message.
    """
    try:
        service = get_calendar_service(user_email)
        event_body = _create_event_body(summary, start, end, description, location, attendees, reminders)
        
        event = service.events().insert(calendarId=calendar_id, body=event_body).execute()
        
        event_id = event.get("id", "")
        event_link = event.get("htmlLink", "")
        logging.info(f"Event created successfully! Event ID: {event_id}")
        return f"Event created successfully!\nEvent ID: {event_id}\nLink: {event_link}"
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to create event. Error: {error}"


def _list_events_impl(calendar_id: str = "primary", time_min: Optional[str] = None,
                     time_max: Optional[str] = None, max_results: int = 10,
                     query: Optional[str] = None, user_email: Optional[str] = None) -> str:
    """Internal implementation for listing events."""
    try:
        service = get_calendar_service(user_email)
        
        # Default to events from now onwards
        if not time_min:
            time_min = datetime.utcnow().isoformat() + "Z"
        else:
            time_min = _parse_datetime(time_min)
            if not time_min.endswith("Z"):
                time_min += "Z"
        
        if time_max:
            time_max = _parse_datetime(time_max)
            if not time_max.endswith("Z"):
                time_max += "Z"
        
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
            q=query
        ).execute()
        
        events = events_result.get("items", [])
        
        if not events:
            return "No events found."
        
        output = [f"Found {len(events)} event(s):\n"]
        for event in events:
            output.append(_format_event(event))
            output.append("-" * 80)
        
        return "\n".join(output)
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to list events. Error: {error}"


@mcp.tool()
def list_events(calendar_id: str = "primary", time_min: Optional[str] = None,
               time_max: Optional[str] = None, max_results: int = 10,
               user_email: Optional[str] = None) -> str:
    """List events from a calendar.
    
    Args:
        calendar_id: Calendar ID (default: "primary").
        time_min: Start time for events (ISO format or natural language).
        time_max: End time for events (ISO format or natural language).
        max_results: Maximum number of events to return (default: 10).
        user_email: Optional email address for multi-account support.
    
    Returns:
        List of events as a formatted string.
    """
    return _list_events_impl(calendar_id, time_min, time_max, max_results, None, user_email)


@mcp.tool()
def search_events(query: str, calendar_id: str = "primary", time_min: Optional[str] = None,
                 time_max: Optional[str] = None, max_results: int = 20,
                 user_email: Optional[str] = None) -> str:
    """Search for events in a calendar.
    
    Args:
        query: Search query (searches in summary, description, location, attendees).
        calendar_id: Calendar ID (default: "primary").
        time_min: Start time for search range.
        time_max: End time for search range.
        max_results: Maximum number of results (default: 20).
        user_email: Optional email address for multi-account support.
    
    Returns:
        Search results as a formatted string.
    """
    return _list_events_impl(calendar_id, time_min, time_max, max_results, query, user_email)


@mcp.tool()
def get_event(event_id: str, calendar_id: str = "primary", user_email: Optional[str] = None) -> str:
    """Get complete details of a specific event.
    
    Args:
        event_id: Event ID.
        calendar_id: Calendar ID (default: "primary").
        user_email: Optional email address for multi-account support.
    
    Returns:
        Complete event details as a formatted string.
    """
    try:
        service = get_calendar_service(user_email)
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        
        return f"""Event Details:
{_format_event(event)}

Created: {event.get('created', 'N/A')}
Updated: {event.get('updated', 'N/A')}
Status: {event.get('status', 'N/A')}
Link: {event.get('htmlLink', 'N/A')}"""
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to get event. Error: {error}"


@mcp.tool()
def update_event(event_id: str, calendar_id: str = "primary", summary: Optional[str] = None,
                start: Optional[str] = None, end: Optional[str] = None,
                description: Optional[str] = None, location: Optional[str] = None,
                user_email: Optional[str] = None) -> str:
    """Update an existing event.
    
    Args:
        event_id: Event ID to update.
        calendar_id: Calendar ID (default: "primary").
        summary: New event title (optional).
        start: New start time (optional).
        end: New end time (optional).
        description: New description (optional).
        location: New location (optional).
        user_email: Optional email address for multi-account support.
    
    Returns:
        Confirmation message.
    """
    try:
        service = get_calendar_service(user_email)
        
        # Get existing event
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        
        # Update fields
        if summary:
            event["summary"] = summary
        if start:
            event["start"] = {"dateTime": _parse_datetime(start), "timeZone": "Asia/Kolkata"}
        if end:
            event["end"] = {"dateTime": _parse_datetime(end), "timeZone": "Asia/Kolkata"}
        if description:
            event["description"] = description
        if location:
            event["location"] = location
        
        updated_event = service.events().update(
            calendarId=calendar_id, eventId=event_id, body=event
        ).execute()
        
        logging.info(f"Event updated successfully! Event ID: {event_id}")
        return f"Event updated successfully!\nEvent ID: {event_id}\nLink: {updated_event.get('htmlLink', '')}"
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to update event. Error: {error}"


@mcp.tool()
def delete_event(event_id: str, calendar_id: str = "primary", user_email: Optional[str] = None) -> str:
    """Delete an event from the calendar.
    
    Args:
        event_id: Event ID to delete.
        calendar_id: Calendar ID (default: "primary").
        user_email: Optional email address for multi-account support.
    
    Returns:
        Confirmation message.
    """
    try:
        service = get_calendar_service(user_email)
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        
        logging.info(f"Event {event_id} deleted successfully!")
        return f"Event {event_id} deleted successfully!"
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to delete event. Error: {error}"


@mcp.tool()
def check_availability(time_min: str, time_max: str, calendar_id: str = "primary",
                      user_email: Optional[str] = None) -> str:
    """Check free/busy times for scheduling.
    
    Args:
        time_min: Start time for availability check.
        time_max: End time for availability check.
        calendar_id: Calendar ID (default: "primary").
        user_email: Optional email address for multi-account support.
    
    Returns:
        Free/busy information as a formatted string.
    """
    try:
        service = get_calendar_service(user_email)
        
        time_min_parsed = _parse_datetime(time_min)
        time_max_parsed = _parse_datetime(time_max)
        
        # Ensure RFC3339 format with 'Z' suffix for UTC
        if not time_min_parsed.endswith('Z'):
            time_min_parsed += 'Z'
        if not time_max_parsed.endswith('Z'):
            time_max_parsed += 'Z'
        
        body = {
            "timeMin": time_min_parsed,
            "timeMax": time_max_parsed,
            "items": [{"id": calendar_id}]
        }
        
        freebusy = service.freebusy().query(body=body).execute()
        
        calendars = freebusy.get("calendars", {})
        calendar_info = calendars.get(calendar_id, {})
        busy_times = calendar_info.get("busy", [])
        
        if not busy_times:
            return f"You are FREE from {time_min} to {time_max}"
        
        output = [f"Busy times from {time_min} to {time_max}:\n"]
        for busy in busy_times:
            start = busy.get("start", "")
            end = busy.get("end", "")
            output.append(f"- {start} to {end}")
        
        return "\n".join(output)
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to check availability. Error: {error}"


@mcp.tool()
def quick_add_event(text: str, calendar_id: str = "primary", user_email: Optional[str] = None) -> str:
    """Quickly add an event using natural language.
    
    Args:
        text: Natural language description (e.g., "Lunch tomorrow at 12pm").
        calendar_id: Calendar ID (default: "primary").
        user_email: Optional email address for multi-account support.
    
    Returns:
        Event ID and confirmation message.
    
    Examples:
        - "Lunch with Sarah next Tuesday at noon"
        - "Team meeting tomorrow 2pm-3pm"
        - "Dentist appointment on Dec 15 at 10am"
    """
    try:
        service = get_calendar_service(user_email)
        event = service.events().quickAdd(calendarId=calendar_id, text=text).execute()
        
        event_id = event.get("id", "")
        event_link = event.get("htmlLink", "")
        logging.info(f"Event created successfully! Event ID: {event_id}")
        return f"Event created successfully!\nEvent ID: {event_id}\nSummary: {event.get('summary', '')}\nLink: {event_link}"
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return f"Failed to create event. Error: {error}"


if __name__ == "__main__":
    # Check if token exists, if not, run OAuth flow
    if not os.path.exists(_get_token_file()):
        logging.info("Token file not found. Starting OAuth flow...")
        try:
            get_calendar_service()
            logging.info("Authentication successful. token.json created.")
        except Exception as e:
            logging.error(f"Error during OAuth flow: {e}")
            exit(1)
    
    logging.info("Starting Calendar MCP Server...")
    asyncio.run(mcp.run_async(transport="stdio"))
