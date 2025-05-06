from calendar_service import get_upcoming_event
from drive_service import check_or_create_folder
from file_fetch import fetch_file_from_api, upload_file_to_drive
from openai_service import get_file_content, summarize_content, upload_summary_as_doc
from email_service import trigger_email_sending  # new Gmail API-based function

# from email_service import send_email_with_attachment

def process_meeting_files():
    try:
        print("Starting Meeting File Processor...")

        # Fetch upcoming event
        event_id, event_title, event_date, event_time, attendee_emails = get_upcoming_event()


        if not event_title or not event_date or not event_time:
            print("No upcoming event found. Exiting.")
            return {"status": "error", "message": "No upcoming event found."}

        print(f"Found Event: {event_title} | Date: {event_date} | Time: {event_time}")

        # Find or create folder in Drive
        folder_id = check_or_create_folder(event_title, event_date, event_time)

        if not folder_id:
            print("No folder found or created. Exiting.")
            return {"status": "error", "message": "Failed to create or find folder."}

        print(f"Folder ID ready: {folder_id}")

        # Fetch file from API
        api_url = "http://127.0.0.1:5050/"  
        file_data, file_name = fetch_file_from_api(api_url)

        if not file_data or not file_name:
            print("Failed to fetch file from API. Exiting.")
            return {"status": "error", "message": "Failed to fetch file from API."}

        # Upload the fetched file into Drive folder
        file_id = upload_file_to_drive(folder_id, file_data, file_name)

        if not file_id:
            print("Upload failed. Exiting.")
            return {"status": "error", "message": "File upload failed."}

        print(f"File '{file_name}' uploaded successfully with ID: {file_id}")

        # Read file content from uploaded file
        file_content = get_file_content(file_id)

        if not file_content:
            print("Could not read uploaded file content. Exiting.")
            return {"status": "error", "message": "Failed to read file content."}

        print("File content read successfully.")

        # Summarize content using OpenAI
        summary = summarize_content(file_content)

        if not summary:
            print("Failed to summarize content. Exiting.")
            return {"status": "error", "message": "Failed to generate summary."}

        print("Summary generated.")

        # Upload summary as Google Docs to Drive
        summary_filename = "Meeting_Summary"
        doc_file_id = upload_summary_as_doc(folder_id, summary, summary_filename)

        if doc_file_id:
            print(f"Summary uploaded successfully as Google Doc with ID: {doc_file_id}")

            # Send the summary as an email attachment to participants
            subject = f"Meeting Summary: {event_title}"
            body = f"Hi team,\n\nPlease find the attached summary for the meeting on {event_date} at {event_time}.\n\nBest,\nAkhila's Assistant"

            #subject = f"Meeting Summary: {event_title}"
            #body = f"Hi team,\n\nPlease find the attached summary for the meeting on {event_date} at {event_time}.\n\nBest,\nAkhila's Assistant "

            #send_email_with_attachment(subject, body, attendee_emails, doc_file_id, "Meeting_Summary.docx")
            trigger_email_sending(subject=subject, body_text=body, recipients=attendee_emails, doc_file_id=doc_file_id, filename="Meeting_Summary.pdf")  # Since you're exporting as PDF from Drive

            return {"status": "success", "message": "Meeting summary sent to participants."}

        else:
            print("Failed to upload summary as Google Doc. Email not sent.")
            return {"status": "error", "message": "Failed to upload summary as Google Doc."}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}
if __name__ == "__main__":
    result = process_meeting_files()
    print(result)