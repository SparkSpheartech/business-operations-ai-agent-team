from google.adk.agents.llm_agent import Agent
from brand_search_optimization.shared_libraries import constants
from brand_search_optimization.tools import bq_connector
from brand_search_optimization import prompt

email_drafter_agent = Agent(
    model=constants.MODEL,
    name="email_drafter",
    description="Professional Email Drafter",
    instruction=prompt.EMAIL_DRAFTER_PROMPT,
    tools=[bq_connector.draft_email]
)
