# 
import asyncio  
import os  
from agents import Runner, set_default_openai_api  
from src.executor_agent.agent import executor_supervisor_agent  
from src.executor_agent.context import ExecutorContext  
from dotenv import load_dotenv  
from src.executor_agent.mcp import get_context7_mcp_server  

  
load_dotenv()  
set_default_openai_api(os.getenv("OPENAI_API_KEY"))  
  
async def main() -> None:

    async with get_context7_mcp_server() as context7_server:
      executor_context = ExecutorContext()  
        
      while True:  
          try:  
              user_input = input(" > ")  
          except (EOFError, KeyboardInterrupt):  
              print()  
              break  
          if user_input.strip().lower() in {"exit", "quit"}:  
              break  
          if not user_input:  
              continue
          
          # executor_agent = executor_supervisor_agent.clone()
          executor_supervisor_agent.mcp_servers = [context7_server]
                
          result = await Runner.run(  
              executor_supervisor_agent,  
              user_input,  
              context=executor_context  
          )  
          print(result.final_output)  
    
if __name__ == "__main__":  
    asyncio.run(main())