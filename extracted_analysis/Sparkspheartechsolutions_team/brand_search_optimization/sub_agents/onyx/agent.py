from google.adk.agents.llm_agent import Agent
from brand_search_optimization.shared_libraries import constants
from brand_search_optimization.tools import bq_connector
from brand_search_optimization import prompt

onyx_agent = Agent(
    model=constants.MODEL,
    name="onyx",
    description="Onyx: The Lead Engineer & Automation Specialist",
    instruction=prompt.ONYX_PROMPT,
    tools=[bq_connector.technical_audit_tool]
)
