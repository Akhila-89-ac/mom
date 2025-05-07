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
  
Project Structure :
minutes-of-meeting-ai/
├── app.py                      # Main orchestration script
├── config.py                   # Configuration constants and paths
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── models/
│   ├── whisper_transcriber.py  # Audio transcription (Whisper)
│   └── speaker_diarizer.py     # Speaker identification (pyannote)
│
├── utils/
│   ├── summarizer.py           # LLM-based summarization
│   └── text_cleaner.py         # Pre-processing transcript text
│
├── integrations/
│   ├── google_calendar.py      # Google Calendar API
│   └── google_drive.py         # Google Drive API
│
├── data/
│   └── sample_audio.wav        # Demo audio file
│
└── output/
    ├── transcript.json
    └── minutes_of_meeting.md



Setup Instructions
1. Clone the Repository
git clone https://github.com/your-username/minutes-of-meeting-ai.git
cd minutes-of-meeting-ai

3. Install Python Dependencies:
pip install -r requirements.txt

3.Set up Google APIs:
Go to https://console.cloud.google.com/
Create a new project
Enable Google Calendar,Google Drive,Gmail and Google Doc APIs in Google Cloud Console
Create an OAuth 2.0 Client ID (Web or Desktop)and download credentials.json and Place it in the project root
On first run, authenticate and token.json will be generated automatically

4.Environment Variables:
Create a .env file in the root directory:
OPENAI_API_KEY=your_openai_key
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
REDIRECT_URI=http://localhost:8080/
EMAIL_SENDER=your_email@gmail.com

5.Set Up Google Cloud Pub/Sub:
Create a Pub/Sub topic and subscription to that topic
Set your Flask webhook URL as the push endpoint in the subscription
Grant the Pub/Sub service account access to invoke your Flask app and read Calendar events

How to Use:
-CLI Mode (Default)
Run from the terminal: python app.py
This will:
Read upcoming calendar events
Check if a folder exists in Google Drive; if not, create it
Wait for a transcript.txt in the folder
Summarize transcript using GPT
Save summary as summary.doc
Share summary.doc with meeting attendees




Sample Input/Output
🔊 Input
.wav or .mp3 meeting recording file in data/

📄 Output
output/transcript.txt → Whisper transcript
output/summary.txt → GPT-generated summary
Google Doc → Shared automatically with participants

✅ You can include screenshots here using:
![Summary Screenshot](screenshots/summary_doc.png)




