import os
from agents import Agent, set_default_openai_api, function_tool
from tavily import AsyncTavilyClient
from dotenv import load_dotenv
from prompt import knowledge_retrieval_agent_prompt
load_dotenv()

set_default_openai_api(os.getenv("OPENAI_API_KEY"))

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
  model="gpt-4.1-nano",
  tools=[web_search],
  instructions=knowledge_retrieval_agent_prompt
)