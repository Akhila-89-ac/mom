import os
import base64
import io
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Define all required Google API scopes
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/gmail.send"
]

def get_services():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    drive_service = build("drive", "v3", credentials=creds)
    gmail_service = build("gmail", "v1", credentials=creds)
    return drive_service, gmail_service

def download_drive_file_as_pdf(drive_service, file_id):
    try:
        request = drive_service.files().export_media(
            fileId=file_id,
            mimeType='application/pdf'
        )
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        fh.seek(0)
        return fh.read()
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None

def trigger_email_sending(subject, body_text, recipients, doc_file_id, filename):
    print("Sending email using Gmail API...")
    drive_service, gmail_service = get_services()

    # Download PDF content
    file_data = download_drive_file_as_pdf(drive_service, doc_file_id)
    if not file_data:
        print("❌ File download failed, email not sent.")
        return

    # Build MIME message
    message = MIMEMultipart()
    message['to'] = ", ".join(recipients)
    message['subject'] = subject

    # Attach body
    message.attach(MIMEText(body_text, 'plain'))

    # Attach file
    part = MIMEBase('application', 'pdf')
    part.set_payload(file_data)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
    message.attach(part)

    # Encode and send
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_result = gmail_service.users().messages().send(
        userId='me',
        body={'raw': raw_message}
    ).execute()

    print("✅ Email sent! Message ID:", send_result['id'])
