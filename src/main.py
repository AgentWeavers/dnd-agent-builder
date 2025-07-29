import asyncio
from agents import run_demo_loop, set_trace_processors
# from planner_agent import planner_supervisor_agent
from planner_agent.subagents.knowledge_retrieval import knowledge_retrieval_agent
# from galileo.handlers.openai_agents import GalileoTracingProcessor


async def main() -> None :
  # set_trace_processors([GalileoTracingProcessor()])
  await run_demo_loop(knowledge_retrieval_agent)
  
if __name__ == "__main__":
  asyncio.run(main())