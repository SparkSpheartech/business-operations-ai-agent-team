from googleapiclient.errors import HttpError
from daisy_executive_assistant.tools.auth import get_drive_service
import io
from googleapiclient.http import MediaIoBaseDownload

def list_recent_drive_files(count: int = 10) -> str:
    """Lists the most recent files modified in Google Drive."""
    try:
        service = get_drive_service()
        results = service.files().list(
            pageSize=count, fields="nextPageToken, files(id, name, mimeType, modifiedTime)",
            orderBy="modifiedTime desc").execute()
        items = results.get('files', [])

        if not items:
            return 'No files found.'
        
        output = []
        for item in items:
            output.append(f"{item['name']} (ID: {item['id']}, Type: {item['mimeType']})")
        return "\\n".join(output)
    except HttpError as error:
        return f'An error occurred: {error}'

def search_drive_files(query_term: str) -> str:
    """Searches for files in Google Drive by name."""
    try:
        service = get_drive_service()
        # Query for name containing term, not trashed
        q = f"name contains '{query_term}' and trashed = false"
        results = service.files().list(
            q=q, pageSize=10, fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])

        if not items:
            return f'No files found matching "{query_term}".'
        
        output = []
        for item in items:
            output.append(f"{item['name']} (ID: {item['id']})")
        return "\\n".join(output)
    except HttpError as error:
        return f'An error occurred: {error}'

def read_drive_file_content(file_id: str) -> str:
    """Reads the text content of a Google Doc or text file."""
    try:
        service = get_drive_service()
        # Check file type
        file_meta = service.files().get(fileId=file_id).execute()
        mime_type = file_meta.get('mimeType')

        if mime_type == 'application/vnd.google-apps.document':
            # Export Google Doc to plain text
            request = service.files().export_media(fileId=file_id, mimeType='text/plain')
        elif mime_type == 'text/plain':
            request = service.files().get_media(fileId=file_id)
        else:
            return f"Cannot read content of file type: {mime_type}. (Only Google Docs and Text files supported currently)"

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        
        return fh.getvalue().decode('utf-8')

    except Exception as error:
        return f'An error occurred reading file: {error}'
