from flask import Flask, request, jsonify
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

app = Flask(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/drive'
]
def get_calendar_service():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    return service
@app.route('/')
def home():
    return 'Hey Akhila! Your Flask app is working'

@app.route('/create-event', methods=['POST'])
def create_event():
    print("Received request!")
    data = request.get_json()
    print(" Input data:", data)

    title = data.get('title')
    description = data.get('description')
    start = data.get('start')
    end = data.get('end')
    attendees = data.get('attendees', [])

    attendee_list = [{'email': email} for email in attendees]

    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': start,
            'timeZone': 'Asia/Kolkata'
        },
        'end': {
            'dateTime': end,
            'timeZone': 'Asia/Kolkata'
        },
        'attendees': attendee_list,
        'conferenceData': {
            'createRequest': {
                'requestId': 'ak-request-id-1234',
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        }
    }

    try:
        
        calendar_service = get_calendar_service()

        created_event = calendar_service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()

        print("Event created with ID:", created_event.get('id'))
    except Exception as e:
        print("Error creating event:", e)
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'message': '🎉 Event created successfully!',
        'eventLink': created_event.get('htmlLink'),
        'meetLink': created_event.get('conferenceData', {}).get('entryPoints', [{}])[0].get('uri')
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8085)

