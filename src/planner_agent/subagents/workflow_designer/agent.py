from agents import Agent
from src.planner_agent.subagents.prompt import agent_tool_workflow_designer_agent_prompt

workflow_designer_agent = Agent(
  name="Agent Tool Workflow Designer",
  model="gpt-4.1-mini",
  instructions=agent_tool_workflow_designer_agent_prompt
)