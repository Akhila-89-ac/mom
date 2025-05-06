# pubsub_handler.py

import json
import base64
from flask import Blueprint, request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime

pubsub_bp = Blueprint("pubsub_bp", __name__)

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive"
]

def get_drive_service():
    try:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        return build("drive", "v3", credentials=creds)
    except Exception as e:
        print(f"❌ Drive Auth Failed: {e}")
        return None

def get_calendar_service():
    try:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        return build("calendar", "v3", credentials=creds)
    except Exception as e:
        print(f"❌ Calendar Auth Failed: {e}")
        return None

@pubsub_bp.route("/pubsub-handler", methods=["POST"])
def handle_pubsub():
    print("\n📬 Pub/Sub Message Received!")

    envelope = request.get_json()
    if not envelope or "message" not in envelope:
        msg = "❌ Invalid Pub/Sub message format"
        print(msg)
        return msg, 400

    try:
        pubsub_message = envelope["message"]
        data = json.loads(base64_decode(pubsub_message["data"]))
        event_id = data.get("eventId")
        print(f"📦 Event ID from Pub/Sub: {event_id}")

        calendar_service = get_calendar_service()
        drive_service = get_drive_service()
        if not calendar_service or not drive_service:
            return "❌ Required service unavailable", 500

        # 🗓️ Fetch full event details
        event = calendar_service.events().get(calendarId="primary", eventId=event_id).execute()
        summary = event.get("summary", "No Title")
        start_time = event.get("start", {}).get("dateTime")

        if not start_time:
            print("❌ No start time found")
            return "Missing start time", 400

        # Format start time
        dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        formatted_time = dt.strftime("%Y-%m-%d %I:%M %p")

        # 📁 Folder name
        folder_name = f"{summary} - {formatted_time}"
        print(f"🗂️ Folder name: {folder_name}")

        # Create folder
        folder_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder"
        }
        folder = drive_service.files().create(body=folder_metadata, fields="id").execute()
        print(f"✅ Folder Created with ID: {folder['id']}")

    except Exception as e:
        print(f"❌ Error handling Pub/Sub: {e}")
        return "Error", 500

    return "OK", 200

def base64_decode(encoded):
    return base64.b64decode(encoded).decode("utf-8")
