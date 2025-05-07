**Minutes of Meeting AI Automation** (MoM-AI)
- An AI-powered automated system that helps you manage your meeting lifecycle from start to finish. It captures your meetings, transcribes them using Whisper, diarizes speakers, summarizes using OpenAI, uploads to Google Drive, and emails participants.

Features
- Auto-creates Google Drive folder when a Google Calendar events with attendees and Meet link is created
- Transcribe meeting audio using OpenAI Whisperr + WhisperX
- Identify speakers using pyannote-audio diarization
- Summarize discussions using LLMs (OpenAI GPT-4o-mini)
- Automatically store transcripts and summaries (google doc) in Google Drive
- share google doc with all attendees via email
- Uses Google Cloud Pub/Sub for scalable automation

Tech Stack
- Python 3.10+
- Flask
- OpenAI API (GPT)
- Whisper
- pyannote-audio (for speaker diarization)
- Google APIs (Calendar, Drive, Docs, Gmail)
- Google Cloud Pub/Sub
  
Project Structure

```text
minutes-of-meeting-ai/
│
├── app.py                   # Main script to orchestrate all steps
├── config.py                # Stores constants and credential paths
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (OPENAI, Google API keys)
│
├── models/
│   ├── whisper_transcriber.py     # Uses Whisper for audio transcription
│   └── speaker_diarizer.py        # Uses pyannote-audio for speaker labels
│
├── utils/
│   ├── summarizer.py              # Summarizes transcripts using LLMs
│   └── text_cleaner.py            # Cleans and formats raw text
│
├── integrations/
│   ├── google_calendar.py         # Google Calendar API integration
│   └── google_drive.py            # Google Drive upload and sharing
│
├── data/
│   └── sample_audio.wav           # Sample audio for testing
│
├── output/
│   ├── transcript.json            # Full transcript with timestamps
│   └── minutes_of_meeting.md      # Final meeting summary
│
└── README.md


Setup Instructions
1. Clone the Repository

git clone https://github.com/your-username/minutes-of-meeting-ai.git
cd minutes-of-meeting-ai
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt

3. Set Up Google APIs
Go to Google Cloud Console

Create a new project

Enable these APIs:

Google Calendar API

Google Drive API

Google Docs API

Gmail API

Create OAuth 2.0 Client ID (Web/Desktop)

Download credentials.json and place it in the project root

On first run, you'll be prompted to authenticate, and token.json will be generated

4. Add Environment Variables
Create a .env file in the root:

env
Copy
Edit
OPENAI_API_KEY=your_openai_key
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
REDIRECT_URI=http://localhost:8080/
EMAIL_SENDER=your_email@gmail.com

5. Set Up Google Cloud Pub/Sub
Create a Pub/Sub topic and a subscription

Set your Flask app's /webhook endpoint as the push endpoint

Grant the Pub/Sub service account permission to:

Push to your Flask endpoint

Read Google Calendar events

In pubsub_handler.py, configure the topic and subscription
How to Use
✅ CLI Mode (default)
bash
Copy
Edit
python app.py
This will:

Fetch the upcoming Google Calendar event

Create a folder in Google Drive (if not exists)

Wait for transcript.txt inside the folder

Summarize the transcript using GPT

Save the summary as summary.docx

Share the document with all meeting participants




📸 Sample Input/Output
🔊 Input
.wav or .mp3 meeting recording file in data/

📄 Output
output/transcript.txt → Whisper transcript

output/summary.txt → GPT-generated summary

Google Doc → Shared automatically with participants

✅ You can include screenshots here using:




