import base64
from email.message import EmailMessage
from googleapiclient.errors import HttpError
from daisy_executive_assistant.tools.auth import get_gmail_service

def send_email(to: str, subject: str, body: str) -> str:
    """Sends an email using the user's Gmail account."""
    try:
        service = get_gmail_service()
        message = EmailMessage()
        message.set_content(body)
        message['To'] = to
        message['Subject'] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }

        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        return f'Message Id: {send_message["id"]} sent successfully.'
    except HttpError as error:
        return f'An error occurred: {error}'

def read_recent_emails(count: int = 5) -> str:
    """Reads the most recent emails from the inbox."""
    # Re-using search_emails for consistency, but keeping this simple wrapper
    return search_emails(query="label:INBOX", max_results=count)

def search_emails(query: str, max_results: int = 10) -> str:
    """Searches using Gmail query format (e.g., 'newer_than:1d', 'from:x', 'is:unread').
    Returns sender, subject, and snippet/body summary.
    """
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])

        if not messages:
            return f"No emails found matching query: '{query}'"

        output = []
        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            payload = txt['payload']
            headers = payload.get("headers", [])
            
            subject = next((i['value'] for i in headers if i["name"] == "Subject"), "No Subject")
            sender = next((i['value'] for i in headers if i["name"] == "From"), "Unknown")
            date = next((i['value'] for i in headers if i["name"] == "Date"), "Unknown Date")
            snippet = txt.get('snippet', '')
            
            # Simple body extraction could go here if snippet isn't enough, 
            # but usually snippet is good for a quick 'analysis'. 
            # If the user needs deep reading, they can use 'read_email_content' (future).
            
            output.append(f"[{date}] (ID: {msg['id']}) From: {sender}\nSubject: {subject}\nSnippet: {snippet}\n---")
        
        return "\n".join(output)

    except HttpError as error:
        return f'An error occurred: {error}'
