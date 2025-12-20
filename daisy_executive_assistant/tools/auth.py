import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes: All previous + Assistant SDK
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/tasks',
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/sdm.service',
    'https://www.googleapis.com/auth/assistant-sdk-prototype' # Google Assistant
]

def get_project_id():
    """Extracts project_id from credentials.json."""
    if not os.path.exists('credentials.json'):
        return None
    try:
        with open('credentials.json', 'r') as f:
            data = json.load(f)
            return data.get('installed', {}).get('project_id')
    except:
        return None

def get_creds():
    """Gets valid user credentials from storage or logs in."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError("credentials.json not found!")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def get_gmail_service():
    return build('gmail', 'v1', credentials=get_creds())

def get_calendar_service():
    return build('calendar', 'v3', credentials=get_creds())

def get_drive_service():
    return build('drive', 'v3', credentials=get_creds())

def get_sheets_service():
    return build('sheets', 'v4', credentials=get_creds())

def get_tasks_service():
    return build('tasks', 'v1', credentials=get_creds())

def get_home_service():
    return build('smartdevicemanagement', 'v1', credentials=get_creds())
