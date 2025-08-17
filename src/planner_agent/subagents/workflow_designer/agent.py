from agents import Agent
from src.planner_agent.subagents.workflow_designer.workflow_prompt import workflow_designer_agent_prompt_v1, workflow_designer_agent_prompt_v3, workflow_designer_agent_prompt_v5

workflow_designer_agent = Agent(
  name="Agent Tool Workflow Designer",
  model="gpt-4.1-mini",
  instructions=workflow_designer_agent_prompt_v3
)