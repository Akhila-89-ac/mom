import json
import uuid
from datetime import datetime, timedelta
from flask import Flask, request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.cloud import pubsub_v1
#from meet import meet_bp
from pubsub_handler import pubsub_bp

app = Flask(__name__)
#app.register_blueprint(meet_bp)
app.register_blueprint(pubsub_bp)

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive"
]

WEBHOOK_URL = "https://bfb5-34-143-150-148.ngrok-free.app/webhook"  # 🔁 Replace when ngrok restarts
PROJECT_ID = "round-folio-457014-a9"
TOPIC_NAME = "calendar-event-topic"

#  Used to avoid duplicate publishing
recent_event_ids = set()

#  Global sync token for Calendar updates
calendar_sync_token = None

#  Load creds for Calendar
def get_calendar_service():
    try:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        return build("calendar", "v3", credentials=creds)
    except Exception as e:
        print(f"❌ Failed to load calendar creds: {e}")
        return None

# 🔐 Load creds for Drive
def get_drive_service():
    try:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        return build("drive", "v3", credentials=creds)
    except Exception as e:
        print(f"❌ Failed to load drive creds: {e}")
        return None

# ✅ Home route
@app.route("/")
def home():
    return "✅ Flask Server Running!"

# 📬 Webhook endpoint
@app.route("/webhook", methods=["POST"])
def calendar_webhook():
    global calendar_sync_token
    print("\n📩 Webhook POST received!")
    print("📩 Headers:", dict(request.headers))

    resource_state = request.headers.get("X-Goog-Resource-State")
    print(f"📣 Resource State: {resource_state}")

    if resource_state == "sync":
        print("🔁 Initial sync received. Skipping.")
        return "", 200

    try:
        service = get_calendar_service()
        if not service:
            return "❌ Calendar service not available", 500

        print("🔍 Checking for changed/new events...")
        if calendar_sync_token:
            events_result = service.events().list(
                calendarId="primary",
                syncToken=calendar_sync_token,
                singleEvents=True
            ).execute()
        else:
            time_min = (datetime.utcnow() - timedelta(minutes=10)).isoformat() + "Z"
            print(f"🕒 First sync fetch from: {time_min}")
            events_result = service.events().list(
                calendarId="primary",
                timeMin=time_min,
                singleEvents=True,
                orderBy="startTime"
            ).execute()

        events = events_result.get("items", [])
        for event in events:
            event_id = event.get("id")
            if is_duplicate(event_id):
                print(f"⚠️ Duplicate skipped: {event_id}")
                continue
            print(f"✅ New/Updated Event: {event_id}")
            publish_to_pubsub(event_id)

        # 🔁 Store syncToken
        if "nextSyncToken" in events_result:
            calendar_sync_token = events_result["nextSyncToken"]
            print("💾 Sync token updated")

    except Exception as e:
        print(f"❌ Error fetching events: {e}")

    return "", 200

# 📤 Pub/Sub Publisher
def publish_to_pubsub(event_id):
    try:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
        message = json.dumps({"eventId": event_id}).encode("utf-8")

        print(f"📨 Sending to Pub/Sub: {event_id}")
        future = publisher.publish(topic_path, data=message)
        result = future.result()
        print(f"✅ Published to Pub/Sub with msg ID: {result}")

    except Exception as e:
        print(f"❌ Pub/Sub publish failed: {e}")


# ❌ Prevent duplicate events
def is_duplicate(event_id):
    if event_id in recent_event_ids:
        return True
    recent_event_ids.add(event_id)
    if len(recent_event_ids) > 100:
        recent_event_ids.pop()
    return False

# 🚀 One-time Calendar subscription
def subscribe_to_calendar():
    service = get_calendar_service()
    if not service:
        print("❌ Cannot subscribe, Calendar service unavailable.")
        return

    channel_id = str(uuid.uuid4())
    body = {
        "id": channel_id,
        "type": "web_hook",
        "address": WEBHOOK_URL,
    }

    try:
        print(f"🛰️ Subscribing with webhook: {WEBHOOK_URL}")
        response = service.events().watch(calendarId="primary", body=body).execute()
        print("✅ Calendar watch started!")
        print(json.dumps(response, indent=2))
    except Exception as e:
        print(f"❌ Subscription error: {e}")

# 🔁 Ensure single subscription setup
subscribed = False

@app.before_request
def setup_once():
    global subscribed
    if not subscribed:
        print("🚀 Setting up Google Calendar subscription...")
        subscribe_to_calendar()
        subscribed = True

# 🏁 Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
