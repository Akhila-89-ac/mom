# Minutes of Meeting AI Automation (MoM-AI)
- An AI-powered automated system that helps you manage your meeting lifecycle from start to finish. It captures your meetings, transcribes them using Whisper, diarizes speakers, summarizes using OpenAI, uploads to Google Drive, and emails participants.
  
## Table of contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Development Software & Tools](#development-software-&-tools)
- [Application Set Up Instructions](#application-set-up-instructions)
- [Project Structure](#project-structure)
- [How to Use](#how-to-use)
- [Sample Input/Output](#sample-input/output)
- 
## Features

- Auto-creates Google Drive folder when a Google Calendar events with attendees and Meet link is created
- Transcribe meeting audio using OpenAI Whisperr + WhisperX
- Identify speakers using pyannote-audio diarization
- Summarize discussions using LLMs (OpenAI GPT-4o-mini)
- Automatically store transcripts and summaries (google doc) in Google Drive
- share google doc with all attendees via email
- Uses Google Cloud Pub/Sub for scalable automation

## Tech Stack

- Python 3.10+
- Flask
- OpenAI API (GPT)
- Whisper
- pyannote-audio (for speaker diarization)
- Google APIs (Calendar, Drive, Docs, Gmail)
- Google Cloud Pub/Sub

## Development Software & Tools

- Python 3.9+
- Flask
- Visual Studio Code (VS Code)
- google cloud shell
- Git & GitHub
- OpenAI API
- Google Cloud Console
– Manage APIs, create OAuth credentials, monitor usage.
- Postman
- Ngrok
  
## Application Set Up Instructions

### 1. Install Python

Before setting up the project, ensure that Python 3.9 or higher is installed on your local machine or development environment.

#### For Local Development (VSCode)

1. Download and install the latest version of Python (Python 3.9 or higher) from the official [Python website](https://www.python.org/downloads/).
2. After installation, verify it by running the following commands in your terminal/command prompt:

   ```python --version```

#### For Google Cloud Shell

Google Cloud Shell already comes with Python pre-installed, so you can skip this step when using Cloud Shell.
   ```python3 --version```
   
### 2. Clone the Repository

To get started, clone the project repository to your local or cloud environment:

```
git clone https://github.com/Akhila-89-ac/minutes-of-meeting-ai.git
cd minutes-of-meeting-ai
```

### 3.Install Dependencies

```pip install -r requirements.txt```
If WhisperX or pyannote-audio require additional installation (e.g., torch, ffmpeg), you may also need:

### 4.Set Up Google APIs & Google Cloud Pub/Sub
- Go to Google Cloud Console
  - Create a new project
- Enable these APIs:
  - Google Calendar API
  - Google Drive API
  - Google Docs API
  - Gmail API
- Create a Pub/Sub topic and a subscription
- Set your Flask app's /webhook endpoint as the push endpoint
- Grant the Pub/Sub service account permission to: Push to your Flask endpoint & Read Google Calendar events

- Create OAuth 2.0 Client ID (Web/Desktop)
- Download credentials.json and place it in the project root
- On first run, you'll be prompted to authenticate, and token.json will be generated

### 5.OpenAI API Setup
- Sign up at https://platform.openai.com
- Generate an API key
- Set it in your .env file:

### 6.Add Environment Variables

Create a .env file in the project root:

```
- OPENAI_API_KEY=your_openai_key
- GOOGLE_CLIENT_ID=your_client_id
- GOOGLE_CLIENT_SECRET=your_client_secret
- REDIRECT_URI=http://localhost:8080/
- EMAIL_SENDER=your_email@gmail.com

```
You can use the python-dotenv package to load these variables into your environment:

```pip install python-dotenv```

### 7.Run the Application

```python app.py```

#### Workflow Pipeline

- Detects new calendar event and creates a corresponding Drive folder
- After meeting, the audio file is uploaded to the Drive folder
- Script fetches the audio, transcribes with WhisperX
- Speaker diarization is done using pyannote-audio
- Full transcript is summarized using OpenAI API
- Summary is saved in the same folder and emailed to participants

### 8.Testing and Debugging

- Test API Endpoints with Postman
- Expose Local Flask Server with Ngrok

### 9.Troubleshooting

- Missing credentials.json: Ensure the credentials file is placed in the root directory of the project.
- Authentication Issues: If token.json is missing, try deleting it and re-authenticating by running the app again.
- Package Issues: Check requirements.txt for any missing packages and install them manually using pip install <package-name>.

## Sample Input/Output

- Input
  - .wav or .mp3 meeting recording file in data/

- Output
  - output/transcript.txt → Whisper transcript
  - output/summary.txt → GPT-generated summary
  - Google Doc → Shared automatically with participants




