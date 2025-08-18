import asyncio
from agents import run_demo_loop
from planner_agent import planner_supervisor_agent



async def main() -> None :
  await run_demo_loop(planner_supervisor_agent)

if __name__ == "__main__":
  asyncio.run(main())