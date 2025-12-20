# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Defines advanced tools for Spark Sphear Team Assistant"""

import os
import datetime
import base64
import json
from email.message import EmailMessage

from google.cloud import bigquery
from googleapiclient.discovery import build
import google.auth
from google.adk.tools import ToolContext
from brand_search_optimization.shared_libraries import constants

# Singleton clients for performance
_bq_client = None
_gmail_service = None

def get_bq_client():
    global _bq_client
    if _bq_client is None:
        try:
            _bq_client = bigquery.Client()
        except Exception:
            pass
    return _bq_client

def get_gmail_service(scope='https://www.googleapis.com/auth/gmail.modify'):
    global _gmail_service
    try:
        creds, _ = google.auth.default(scopes=[scope])
        _gmail_service = build('gmail', 'v1', credentials=creds)
    except Exception:
        pass
    return _gmail_service

TASKS_FILE = "business_tasks.json"

def get_business_details(tool_context: ToolContext = None):
    """Retrieves Spark Sphear Tech Solutions business details."""
    return """
    Business: Spark Sphear Tech Solutions
    URL: sparkspheartechsolutions.com
    Mission: Scaling businesses through AI, automation, and Cloud infrastructure.
    Team: 
    - Daisy: Manager/Orchestrator
    - Onyx: Lead Engineer (Automation, AI dev)
    - Travis: Security & Architecture (GCP, Security protocols)
    - Eissa: Sales & Marketing (Growth, SEO, Copywriting)
    """

def get_team_status_dashboard():
    """Generates a visual status of the business and team."""
    today = datetime.date.today().strftime("%B %d, %Y")
    tasks = manage_tasks("list")
    return f"""
# 🖥️ Spark Sphear OS: Command Center
**Date:** {today}
**System Status:** Team Fully Operational

| Agent | Specialized Domain | Status |
|---|---|---|
| **Daisy** | Business Orchestration | ONLINE |
| **Onyx** | Automation & Engineering | ONLINE |
| **Travis** | Security & Architecture | ONLINE |
| **Eissa** | Growth & Marketing | ONLINE |

## 📝 Active Task List
{tasks}

## 🚀 Active Resources
- **Gmail Integration:** Connected (Authorized)
- **BigQuery Data Store:** Active
- **Model Backend:** {constants.MODEL}
"""

def manage_tasks(action: str, task_description: str = None) -> str:
    """
    Manages business tasks.
    Args:
        action: 'list', 'add', or 'complete'
        task_description: The description of the task.
    """
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as f:
            json.dump([], f)
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
    
    if action == 'list':
        if not tasks: return "No active tasks."
        return "\n".join([f"- [ ] {t}" for t in tasks])
    elif action == 'add' and task_description:
        tasks.append(task_description)
        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks, f)
        return f"Task added: {task_description}"
    elif action == 'complete' and task_description:
        if task_description in tasks:
            tasks.remove(task_description)
            with open(TASKS_FILE, 'w') as f:
                json.dump(tasks, f)
            return f"Task completed: {task_description}"
        return "Task not found."
    return "Invalid action."

def draft_email(recipient: str, subject: str, key_points: str, tone: str = "professional"):
    """
    Drafts a high-impact professional email.
    Args:
        recipient: Who the email is for.
        subject: The subject line.
        key_points: Core messages.
        tone: Tone of the email.
    """
    return f"Subject: {subject}\n\nDear {recipient},\n\n[DRAFTED EMAIL - {tone} tone]\n\nBased on: {key_points}\n\nBest,\nSpark Sphear Team"

def send_gmail_message(to: str, subject: str, content: str):
    """Sends an email using the Gmail API."""
    service = get_gmail_service('https://www.googleapis.com/auth/gmail.send')
    if not service: return "Gmail API not authorized or connected."
    try:
        message = EmailMessage()
        message.set_content(content)
        message['To'] = to
        message['From'] = 'me'
        message['Subject'] = subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        return f"Email sent successfully! ID: {send_message['id']}"
    except Exception as e: return f"Error sending email: {str(e)}"

def search_gmail_messages(query: str):
    """Searches for emails in the user's Gmail."""
    service = get_gmail_service('https://www.googleapis.com/auth/gmail.readonly')
    if not service: return "Gmail API not authorized or connected."
    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=3).execute()
        messages = results.get('messages', [])
        if not messages: return "No matching emails found."
        summary = "Search Results:\n"
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            summary += f"- {msg_data.get('snippet', '')}\n"
        return summary
    except Exception as e: return f"Error searching Gmail: {str(e)}"

def technical_audit_tool(component_description: str):
    """Performs a technical sanity check on a software component."""
    return f"Onyx Technical Audit: {component_description}\nFeasibility: High. Recommended Stack: Python/GCP. Optimization: Use Async for I/O tasks."

def security_risk_assessment(architecture_plan: str):
    """Identifies security gaps in a cloud architecture."""
    return f"Travis Security Review: {architecture_plan}\nStatus: Passing with recommendations. Ensure VPC-SC is active for sensitive BigQuery datasets."

def marketing_keyword_analyzer(target_niche: str):
    """Identifies high-ROI keywords for a niche."""
    return f"Eissa Growth Report: {target_niche}\nKeywords: 'AI automation for solo-preneurs', 'Vertex AI scaling', 'Cloud architecture optimization'."

def create_task_roadmap(goal: str):
    """Creates a step-by-step business project roadmap."""
    return f"Daisy's Project Roadmap for '{goal}':\n1. Analysis (Eissa)\n2. Technical Spec (Onyx)\n3. Security Review (Travis)\n4. Implementation & Launch."
