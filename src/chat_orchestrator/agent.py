from agents import Agent, ItemHelpers, MessageOutputItem, RunContextWrapper, ToolCallItem, ToolCallOutputItem, TResponseInputItem, function_tool, handoff, trace

from src.planner_agent.agent import planner_supervisor_agent

chat_agent = Agent(
    name="chat_agent",
    # handoff_description="A agent that can delegate the user request to appropriate agents",
    instructions=(
        # f"{RECOMMENDED_PROMPT_PREFIX}"
        "An agent that can chat with the user and answer questions"
    ),
    tools=[
      planner_supervisor_agent.as_tool(
        tool_name="planner_supervisor_agent",
        tool_description="A agent that can delegate the user request to appropriate agents"
      )
    ],
    handoffs=[],
    model="gpt-4.1-mini"
)