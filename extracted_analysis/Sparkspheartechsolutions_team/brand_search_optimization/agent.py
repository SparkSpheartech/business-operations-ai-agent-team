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

"""Defines the Spark Sphear Team Assistant with Parallel Processing"""

from google.adk.agents.llm_agent import Agent
from google.adk.agents.parallel_agent import ParallelAgent

from brand_search_optimization.shared_libraries import constants
from brand_search_optimization.sub_agents.onyx.agent import onyx_agent
from brand_search_optimization.sub_agents.travis.agent import travis_agent
from brand_search_optimization.sub_agents.eissa.agent import eissa_agent
from brand_search_optimization.sub_agents.email_drafter.agent import email_drafter_agent
from brand_search_optimization.tools import bq_connector

from brand_search_optimization import prompt

# The Team Huddle: This allows Eissa, Onyx, and Travis to work in parallel
team_huddle = ParallelAgent(
    name="team_huddle",
    description="A parallel huddle where the whole team analyzes a goal at once.",
    agents=[onyx_agent, travis_agent, eissa_agent]
)

root_agent = Agent(
    model=constants.MODEL,
    name="daisy",
    description="Daisy: Spark Sphear's Business Manager & Lead Assistant",
    instruction=prompt.ROOT_PROMPT,
    sub_agents=[
        team_huddle, 
        onyx_agent,
        travis_agent,
        eissa_agent,
        email_drafter_agent,
    ],
    tools=[
        bq_connector.get_business_details,
        bq_connector.get_team_status_dashboard,
        bq_connector.manage_tasks,
        bq_connector.create_task_roadmap,
        bq_connector.send_gmail_message,
        bq_connector.search_gmail_messages,
    ]
)

from google.adk.apps.app import App

app = App(root_agent=root_agent, name="spark_sphear_team")
