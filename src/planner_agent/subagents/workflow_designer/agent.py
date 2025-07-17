import os
from agents import Agent, set_default_openai_api
from dotenv import load_dotenv
from prompt import agent_tool_workflow_designer_agent_prompt
load_dotenv()

set_default_openai_api(os.getenv("OPENAI_API_KEY"))

workflow_designer_agent = Agent(
  name="Agent Tool Workflow Designer",
  model="gpt-4.1-mini",
  instructions=agent_tool_workflow_designer_agent_prompt
)