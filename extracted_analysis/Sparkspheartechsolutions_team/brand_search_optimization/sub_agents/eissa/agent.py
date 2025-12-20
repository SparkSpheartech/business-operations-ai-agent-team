from google.adk.agents.llm_agent import Agent
from brand_search_optimization.shared_libraries import constants
from brand_search_optimization.tools import bq_connector
from brand_search_optimization import prompt

eissa_agent = Agent(
    model=constants.MODEL,
    name="eissa",
    description="Eissa: Sales & Marketing Growth Engine",
    instruction=prompt.EISSA_PROMPT,
    tools=[
        bq_connector.get_business_details,
        bq_connector.marketing_keyword_analyzer
    ]
)
