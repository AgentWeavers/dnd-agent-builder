from agents import handoff, HandoffInputData, HandoffInputFilter
from agents.extensions.handoff_filters import remove_all_tools

from src.executor_agent.agent import executor_supervisor_agent
from src.planner_agent.agent import planner_supervisor_agent

planner_to_executor = handoff(
  agent=executor_supervisor_agent,
  input_filter=remove_all_tools,
  # tool_description="Transfer back to executor supervisor for agent plan execution"
)

executor_to_planner = handoff(
  agent=planner_supervisor_agent,
  input_filter=remove_all_tools,
  # tool_description="Transfer back to planner supervisor for specification refinement or clarification"  
)

planner_supervisor_agent.handoffs.append(planner_to_executor)
executor_supervisor_agent.handoffs.append(executor_to_planner)
