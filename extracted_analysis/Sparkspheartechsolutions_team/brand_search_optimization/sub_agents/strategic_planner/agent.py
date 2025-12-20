from google.adk.agents.llm_agent import Agent
from ...shared_libraries import constants
from ...tools import bq_connector
from ... import prompt

strategic_planner_agent = Agent(
    model=constants.MODEL,
    name="strategic_planner_agent",
    description="Strategic planning and business scaling agent",
    instruction=prompt.STRATEGIC_PLANNER_PROMPT,
    tools=[
        bq_connector.get_business_details,
    ],
)
