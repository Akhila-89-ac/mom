from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_upcoming_event():
    service = get_calendar_service()
    now = datetime.utcnow().isoformat() + 'Z'  
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=1, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print("No upcoming events found.")
        return None, None, None, None

    event = events[0]
    event_id = event['id']
    event_title = event['summary']

    
    event_start = event['start'].get('dateTime', event['start'].get('date'))
    event_date_time = datetime.fromisoformat(event_start)

    event_date = event_date_time.strftime("%Y-%m-%d")  
    event_time = event_date_time.strftime("%I:%M %p")  

    print(f"Found event: {event_title} (ID: {event_id})")
    print(f"Event Date: {event_date}")
    print(f"Event Time: {event_time}")

    # Extract attendee emails
    attendees = event.get('attendees', [])
    attendee_emails = [att['email'] for att in attendees if 'email' in att]

    return event_id, event_title, event_date, event_time, attendee_emails
