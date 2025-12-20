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

import json
import os
from google.adk.tools import ToolContext

TASKS_FILE = "business_tasks.json"

def manage_tasks(action: str, task_description: str = None) -> str:
    """
    Manages business tasks for the solo-preneur.
    
    Args:
        action: 'list', 'add', or 'complete'
        task_description: The description of the task to add or complete.
    """
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as f:
            json.dump([], f)
    
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
        
    if action == 'list':
        if not tasks: return "No active tasks. Time to scale!"
        return "\n".join([f"- [ ] {t}" for t in tasks])
    
    elif action == 'add' and task_description:
        tasks.append(task_description)
        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks, f)
        return f"Added task: {task_description}"
    
    elif action == 'complete' and task_description:
        if task_description in tasks:
            tasks.remove(task_description)
            with open(TASKS_FILE, 'w') as f:
                json.dump(tasks, f)
            return f"Completed task: {task_description}"
        return "Task not found."
    
    return "Invalid action."
