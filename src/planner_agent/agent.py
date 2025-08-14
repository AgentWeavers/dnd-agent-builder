from agents import Agent, function_tool
from src.planner_agent.subagents.intent_analyzer import intent_analyzer_agent
from src.planner_agent.subagents.knowledge_retrieval import knowledge_retrieval_agent
from src.planner_agent.subagents.workflow_designer.agent import workflow_designer_agent
from src.planner_agent.supervisor_prompt import supervisor_agent_prompt_v2

@function_tool
def think(thought: str) -> str:
  """
  Use this tool to think step-by-step, break down complex problems, plan execution, 
  or outline the structure of your response, especially before generating complex outputs like JSON. 
  This helps ensure thorough reasoning and accurate results. It does not interact with the outside 
  world or retrieve new information.
  """
  print(f"--- Thinking --- \n{thought}\n---")
  return "Thought process recorded."

def get_prompt() -> str:
  return supervisor_agent_prompt_v2

planner_supervisor_agent = Agent(
  name="Planner Supervisor",
  instructions=get_prompt(),
  model="gpt-4.1-mini",
  tools=[
    think, 
    intent_analyzer_agent.as_tool(
      tool_name="intent_analyzer",
      tool_description="Requirements Analysis Agent, responsible for defining clear, specific purposes and performing comprehensive analysis for AI agents."
    ),
    knowledge_retrieval_agent.as_tool(
      tool_name="knowledge_retrieval",
      tool_description="Knowledge Retrieval Agent, responsible for searching the web for information related to the given query."
    ),
    workflow_designer_agent.as_tool(
      tool_name="architecture_tool_workflow_designer",
      tool_description="The Agent Tool Workflow Designer plans agent architectures, specifies tools, and designs workflows to ensure robust, scalable, and effective AI agent solutions."
    ),
  ],  
)