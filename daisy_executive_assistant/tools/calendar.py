import datetime
from googleapiclient.errors import HttpError
from daisy_executive_assistant.tools.auth import get_calendar_service

def list_calendars() -> str:
    """Lists all calendars the user has access to."""
    try:
        service = get_calendar_service()
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])

        if not calendars:
            return 'No calendars found.'

        output = []
        for calendar in calendars:
            summary = calendar.get('summary', 'Unknown')
            cal_id = calendar.get('id', 'Unknown')
            primary = " (Primary)" if calendar.get('primary') else ""
            output.append(f"- {summary} (ID: {cal_id}){primary}")
        
        return "Available Calendars:\n" + "\n".join(output)

    except HttpError as error:
        return f'An error occurred: {error}'

def list_upcoming_events(count: int = 10, calendar_id: str = 'primary') -> str:
    """Lists the next upcoming events on a specific calendar (default: primary)."""
    try:
        service = get_calendar_service()
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                              maxResults=count, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return f'No upcoming events found on calendar {calendar_id}.'

        output = [f"Upcoming events for calendar '{calendar_id}':"]
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_id = event.get('id')
            summary = event.get('summary', '(No Title)')
            output.append(f"- [{start}] {summary} (ID: {event_id})")
        return "\n".join(output)

    except HttpError as error:
        return f'An error occurred: {error}'

def create_calendar_event(summary: str, start_time_iso: str, end_time_iso: str, calendar_id: str = 'primary', description: str = None) -> str:
    """Creates a new event on a specific calendar.
    Time format must be ISO 8601, e.g., '2023-10-25T09:00:00-07:00'.
    """
    try:
        service = get_calendar_service()
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time_iso,
                'timeZone': 'UTC', # Defaulting to UTC/User's local if specified in offset
            },
            'end': {
                'dateTime': end_time_iso,
                'timeZone': 'UTC',
            },
        }

        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        return f"Event created: {event.get('htmlLink')}"

    except HttpError as error:
        return f'An error occurred: {error}'

def update_calendar_event(event_id: str, calendar_id: str = 'primary', summary: str = None, description: str = None) -> str:
    """Updates an existing event. Only updates provided fields."""
    try:
        service = get_calendar_service()
        # First retrieve the event to get its current state and sequence number
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

        if summary:
            event['summary'] = summary
        if description:
            event['description'] = description

        updated_event = service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
        return f"Event updated: {updated_event.get('htmlLink')}"

    except HttpError as error:
        return f'An error occurred: {error}'

def delete_calendar_event(event_id: str, calendar_id: str = 'primary') -> str:
    """Deletes an event from a specific calendar."""
    try:
        service = get_calendar_service()
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        return f"Event {event_id} deleted successfully from calendar {calendar_id}."

    except HttpError as error:
        return f'An error occurred: {error}'
