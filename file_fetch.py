import requests
import io
from googleapiclient.http import MediaIoBaseUpload
from drive_service import get_drive_service

def fetch_file_from_api(api_url):
    
    print(" Fetching file from API...")
    response = requests.get(api_url)

    if response.status_code == 200:
        file_data = response.content
        file_name = response.headers.get('Content-Disposition', 'filename=default_file').split('=')[1]
        print(f"File fetched successfully: {file_name}")
        return file_data, file_name
    else:
        print(f"Failed to fetch file. Status code: {response.status_code}")
        return None, None

def upload_file_to_drive(folder_id, file_data, file_name):
    
    print(" Uploading file to Google Drive...")
    drive_service = get_drive_service()

    file_io = io.BytesIO(file_data)
    media = MediaIoBaseUpload(file_io, mimetype='application/octet-stream')

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    file = drive_service.files().create(
        media_body=media,
        body=file_metadata,
        fields='id'
    ).execute()

    print(f"File uploaded successfully with ID: {file['id']}")
    return file['id']
