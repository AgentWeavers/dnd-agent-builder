import os
from agents import Agent, function_tool
from tavily import AsyncTavilyClient
from dotenv import load_dotenv
from src.planner_agent.subagents.knowledge_retrieval.knowledge_retrieval_prompt import knowledge_retrieval_agent_prompt_v1
from src.deep_research_agent.agent import create_main_orchestrator_agent

load_dotenv()

@function_tool
async def web_search(query: str) -> dict:
  """Do web search on a given topic for the most relevant and up-to-date information. Use this tool when you need comprehensive information on a specific framework, tool, pattern, or implementation approach.

  Args:
      query (str): The topic to search for

  Returns:
      dict: The search results as returned by Tavily API
  """
  tavily_client = AsyncTavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
  search_results = await tavily_client.search(query)
  return search_results

knowledge_retrieval_agent = Agent(
  name="Knowledge Retrieval Agent",
  model="gpt-4.1-mini",
  tools=[
    web_search,       
    create_main_orchestrator_agent().as_tool(
      tool_name="deep_research_orchestrator",
      tool_description="The Deep Research Orchestrator is responsible for orchestrating the deep research process, including the use of tools to conduct research and generate a final report."
    )],
  instructions=knowledge_retrieval_agent_prompt_v1
)