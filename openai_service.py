import io
import os
import openai
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
load_dotenv("/home/akhila8452/mom_auth/.env")



SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/calendar"]
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_drive_service():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("drive", "v3", credentials=creds), build("docs", "v1", credentials=creds)


def get_file_content(file_id):
    try:
        print("Connecting to Google Drive to fetch file...")
        # Initialize the drive service properly here
        drive_service, _ = get_drive_service()  # Get drive service here
        
        request = drive_service.files().get_media(fileId=file_id)
        file_data = io.BytesIO()
        downloader = MediaIoBaseDownload(file_data, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()

        file_data.seek(0)
        content = file_data.read().decode('utf-8')

        print("File content fetched successfully.")
        return content

    except Exception as e:
        print(f"Error reading file from Drive: {e}")
        return None


# Summarize content using OpenAI
def summarize_content(content):
    try:
        print("Sending file content to OpenAI for summarization...")
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """You are an advanced AI-powered meeting assistant assigned to extract key insights, decisions, and action items from business, project, technical, sales, and finance meetings.

## Your Responsibilities:
- Identify meeting type
- Extract key points
- Generate clear summaries
- Provide action items

## Output Structure:
1. **Meeting Summary** (include attendees if available)
2. **Key Insights & Takeaways**
3. **Decisions Made**
4. **Action Items (with deadlines)**
5. **Pending Issues**
6. **Discussion Details** (time-stamped if possible)
7. **Technical Terms & Insights**

Make it clean, professional, and easy to understand.
"""}, 
                {"role": "user", "content": content}
            ]
        )

        summary = response.choices[0].message['content'].strip()
        print("Summarization completed successfully.")
        return summary

    except Exception as e:
        print(f"Error generating summary with OpenAI: {e}")
        return None

def upload_summary_as_doc(folder_id, summary_text, doc_title="Meeting Summary"):
    try:
        print("📄 Creating Google Doc with summary...")

        # ✅ FIXED: Get services using helper function
        drive_service, docs_service = get_drive_service()

        file_metadata = {
            'name': doc_title,
            'mimeType': 'application/vnd.google-apps.document',
            'parents': [folder_id]
        }

        file = drive_service.files().create(body=file_metadata, fields='id').execute()
        doc_file_id = file.get('id')   
        print(f"Google Doc created with ID: {doc_file_id}")

        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': summary_text
                }
            }
        ]

        docs_service.documents().batchUpdate(documentId=doc_file_id, body={'requests': requests}).execute()
        print("Summary text inserted into Google Doc successfully.")

        return doc_file_id

    except Exception as e:
        print(f"Error uploading summary as Google Doc: {e}")
        return None



