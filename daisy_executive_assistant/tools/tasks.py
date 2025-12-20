from googleapiclient.errors import HttpError
from daisy_executive_assistant.tools.auth import get_tasks_service

def get_default_tasklist_id() -> str:
    """Helper to get the ID of the first task list (usually 'My Tasks')."""
    service = get_tasks_service()
    results = service.tasklists().list(maxResults=1).execute()
    items = results.get('items', [])
    if not items:
        # Create one if none exist? Rarely happens.
        return '@default' 
    return items[0]['id']

def list_tasks(tasklist_id: str = '@default') -> str:
    """Lists pending tasks from a task list."""
    try:
        service = get_tasks_service()
        results = service.tasks().list(tasklist=tasklist_id, showCompleted=False, maxResults=20).execute()
        items = results.get('items', [])

        if not items:
            return 'No pending tasks found.'

        output = []
        for item in items:
            due = f" (Due: {item.get('due')[:10]})" if item.get('due') else ""
            output.append(f"[{item['title']}]{due} - ID: {item['id']}")
        return "\\n".join(output)
    except HttpError as error:
        return f'An error occurred: {error}'

def create_task(title: str, notes: str = "", due_date: str = None) -> str:
    """Creates a new task. due_date in UTC RFC3339 format (optional)."""
    try:
        service = get_tasks_service()
        task = {
            'title': title,
            'notes': notes
        }
        if due_date:
            task['due'] = due_date

        result = service.tasks().insert(tasklist='@default', body=task).execute()
        return f"Task created: {result['title']} (ID: {result['id']})"
    except HttpError as error:
        return f'An error occurred: {error}'

def complete_task(task_id: str) -> str:
    """Marks a task as completed."""
    try:
        service = get_tasks_service()
        # To complete, we must update status to 'completed'
        task = service.tasks().get(tasklist='@default', task=task_id).execute()
        task['status'] = 'completed'
        service.tasks().update(tasklist='@default', task=task_id, body=task).execute()
        return f"Task '{task['title']}' marked as completed."
    except HttpError as error:
        return f'An error occurred: {error}'
