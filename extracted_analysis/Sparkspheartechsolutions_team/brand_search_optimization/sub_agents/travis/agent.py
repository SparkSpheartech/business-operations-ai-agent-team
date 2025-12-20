from google.adk.agents.llm_agent import Agent
from brand_search_optimization.shared_libraries import constants
from brand_search_optimization.tools import bq_connector
from brand_search_optimization import prompt

travis_agent = Agent(
    model=constants.MODEL,
    name="travis",
    description="Travis: Security & Architecture Guardian",
    instruction=prompt.TRAVIS_PROMPT,
    tools=[bq_connector.security_risk_assessment]
)
