from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

def check_or_create_folder(event_title, event_date, event_time):
    drive_service = get_drive_service()

    folder_name = f"{event_title} - {event_date} {event_time}"

    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get('files', [])

    if folders:
        folder_id = folders[0]['id']
        print(f"Folder '{folder_name}' found with ID: {folder_id}")
        return folder_id
    

    else:
        print(f"Folder '{folder_name}' not found. Creating a new one...")
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder['id']
        print(f"New folder '{folder_name}' created with ID: {folder_id}")
        return folder_id
