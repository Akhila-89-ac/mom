import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
import io
from dotenv import load_dotenv
load_dotenv("/home/akhila8452/mom_auth/.env")


SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/calendar"]
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def get_drive_service():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("drive", "v3", credentials=creds), build("docs", "v1", credentials=creds)

def download_drive_file(doc_file_id, filename):
    try:
        drive_service, _ = get_drive_service()
        request = drive_service.files().export_media(
            fileId=doc_file_id,
            mimeType='application/pdf'  # or .docx
        )
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

        fh.seek(0)
        return fh.read()
    except Exception as e:
        print(f"Error downloading file from Drive: {e}")
        return None



def send_email_with_attachment(subject, body, recipients, doc_file_id, filename):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    
    file_data = download_drive_file(doc_file_id, filename)

    if file_data:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file_data)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(part)
    else:
        print("File download failed, sending email without attachment.")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipients, msg.as_string())

    print("✅ Email with attachment sent.")
