from google.adk.agents import Agent
# from google.adk.tools import google_search
from jayden_marketing_assistant.agent import root_agent as jayden
from onyx_engineer.agent import root_agent as onyx
from daisy_executive_assistant.tools.gmail import send_email, read_recent_emails, search_emails
from daisy_executive_assistant.tools.calendar import list_upcoming_events, create_calendar_event, list_calendars, update_calendar_event, delete_calendar_event
from daisy_executive_assistant.tools.drive import list_recent_drive_files, search_drive_files, read_drive_file_content
from daisy_executive_assistant.tools.sheets import read_spreadsheet_values, append_spreadsheet_row, create_spreadsheet
from daisy_executive_assistant.tools.tasks import list_tasks, create_task, complete_task
from daisy_executive_assistant.tools.vertex import get_vertex_model_response, list_vertex_models
from daisy_executive_assistant.tools.home import list_smart_home_devices, execute_device_command
from daisy_executive_assistant.tools.assistant import ask_google_assistant, broadcast_message
import daisy_executive_assistant.tools.db as db

# 1. Initialize DB and Context
db.init_db()
last_context = db.get_last_conversation("daisy_executive_assistant", limit=5)
greeting = "Hi Shazaly, how are you?"
if last_context:
    # Simulating a "thought" process to generate a better greeting based on history
    # Ideally, we would ask the LLM to generate this, but for now we'll append the context.
    # To truly "state something from our last conversation", we can just inject it or use the LLM once.
    # Let's use get_vertex_model_response for this specific startup task if possible, or just standard prompt injection.
    
    prompt = f"""
    The user is starting a new session.
    Here is the last conversation history:
    {last_context}
    
    Generate a short, friendly greeting (1-2 sentences).
    Mention what we talked about last time and ask if we should continue that or start something new.
    """
    # Using existing tool to get the greeting dynamically
    try:
        greeting = get_vertex_model_response(prompt, model_name="gemini-pro")
    except:
        greeting = f"Hi Shazaly! Last time we were discussing: {last_context[:50]}... Should we continue?"

# 2. Setup Persona
try:
    with open('daisy_executive_assistant/About Daisy/Daisy_Persona.txt', 'r') as f:
        persona = f.read()
except:
    persona = "You are an Executive Assistant."

instruction = f"""
{persona}

**User Context:**
You are the Executive Assistant to **Shazaly**, the CEO.
You know his name is Shazaly.
You are helpful, proactive, and professional.

**Team Access:**
You have access to the following team members (agents):
1. **Jayden**: Marketing Assistant.
2. **Onyx**: Engineering/Tech Assistant.

**Memory & Continuity:**
- **Startup Greeting**: You have just started up. Your initial thought/greeting was: "{greeting}".
- **Persistence**: You MUST save important interactions to the database using the `save_to_memory` tool.
- **Context**: Use the history of your conversations to provide a seamless experience.

**Tools:**
You have access to Shazaly's **Google Workspace**:
- **Gmail**: Read emails, send/draft emails.
- **Calendar**: Check upcoming events, schedule new meetings.
- **Drive**: Search for files, list recent files, and read Google Docs/text files.
- **Sheets**: Read data from sheets, append new rows, or create new spreadsheets.
- **Tasks**: Manage To-do lists (Add/List/Complete tasks).
- **Google Search**: Check Weather, News, Info.
- **Vertex AI**: Access Google's Cloud AI models directly.
- **Smart Home**: List connected devices and send commands (SDM API).
- **Google Assistant**: Send text commands or broadcasts (Requires Device Model registration).

**Instructions:**
- Proactively manage tasks. If the CEO asks you to "remind him" to do something, add it to his Tasks.
- **Email Analysis**: When asked to analyze emails for a specific time (e.g., "today", "this month"), use `search_emails` with Gmail search operators:
    - Today: `newer_than:1d`
    - Specific Month: `after:2023/12/01 before:2024/01/01`
    - Important: `is:important` or `label:starred`
    - **Always** use `search_emails` for these requests, not `read_recent_emails`.
- **Memory**: CALL `save_to_memory` after every significant turn to ensure we remember this for next time.
"""

# Wrapper tool to expose DB save to the agent
def save_to_memory(content: str):
    """Saves the current conversation turn or important details to long-term memory."""
    db.save_message("daisy_executive_assistant", "user/assistant", content)
    return "Saved to memory."

root_agent = Agent(
    name='daisy_executive_assistant',
    model='gemini-2.0-flash',
    instruction=instruction,
    sub_agents=[jayden, onyx],
    tools=[
        send_email, read_recent_emails, search_emails,
        list_upcoming_events, create_calendar_event, list_calendars, update_calendar_event, delete_calendar_event,
        list_recent_drive_files, search_drive_files, read_drive_file_content,
        read_spreadsheet_values, append_spreadsheet_row, create_spreadsheet,
        list_tasks, create_task, complete_task,
        get_vertex_model_response, list_vertex_models,
        list_smart_home_devices, execute_device_command,
        ask_google_assistant, broadcast_message,
        save_to_memory # Register the memory tool
        # google_search
    ]
)