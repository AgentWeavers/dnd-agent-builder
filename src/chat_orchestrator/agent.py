import os
from agents import Agent, ItemHelpers, MessageOutputItem, RunContextWrapper, ToolCallItem, ToolCallOutputItem, TResponseInputItem, function_tool, handoff, trace, set_default_openai_api

from dotenv import load_dotenv

load_dotenv()

set_default_openai_api(os.getenv("OPENAI_API_KEY"))


chat_agent = Agent(
    name="chat_agent",
    # handoff_description="A agent that can delegate the user request to appropriate agents",
    instructions=(
        # f"{RECOMMENDED_PROMPT_PREFIX}"
        "An agent that can chat with the user and answer questions"
    ),
    tools=[],
    handoffs=[],
    model="gpt-4.1-mini"
)