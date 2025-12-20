from googleapiclient.errors import HttpError
from daisy_executive_assistant.tools.auth import get_sheets_service

def read_spreadsheet_values(spreadsheet_id: str, range_name: str) -> str:
    """Reads values from a specific range in a Google Sheet."""
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=range_name).execute()
        values = result.get('values', [])

        if not values:
            return 'No data found.'

        output = []
        for row in values:
            output.append(", ".join(row))
        return "\\n".join(output)
    except HttpError as error:
        return f'An error occurred: {error}'

def append_spreadsheet_row(spreadsheet_id: str, range_name: str, values: list[str]) -> str:
    """Appends a row of data to a spreadsheet."""
    try:
        service = get_sheets_service()
        body = {
            'values': [values]
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        
        updates = result.get('updates', {})
        return f"{updates.get('updatedCells')} cells updated."
    except HttpError as error:
        return f'An error occurred: {error}'

def create_spreadsheet(title: str) -> str:
    """Creates a new Google Spreadsheet."""
    try:
        service = get_sheets_service()
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                    fields='spreadsheetId').execute()
        return f"Spreadsheet created. ID: {spreadsheet.get('spreadsheetId')}"
    except HttpError as error:
        return f'An error occurred: {error}'
