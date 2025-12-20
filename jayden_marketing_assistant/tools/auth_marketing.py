import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes for Blogger (and potentially others in the future)
SCOPES = ['https://www.googleapis.com/auth/blogger']

TOKEN_FILE = 'token_marketing.json' # SEPARATE token file for the marketing email!

def get_marketing_creds():
    """Gets credentials for the Marketing account (sparkspheartech4me)."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError("credentials.json not found!")
            
            # Use the same client secrets, but store to a DIFFERENT token file
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            
            print(f"--- MARKETING AUTH REQURIED ---")
            print(f"Please log in with: sparkspheartech4me@gmail.com")
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return creds

def get_blogger_service():
    return build('blogger', 'v3', credentials=get_marketing_creds())
