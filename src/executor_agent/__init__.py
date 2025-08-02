"""
Executor Agent Package

This package provides an Executor agent that takes plans from the Planner agent and creates
actual agent implementations using the OpenAI Agents SDK.
"""

from .agent import executor_supervisor_agent
from .models import (
    AgentSpecification,
)

__all__ = [
    "executor_supervisor_agent",
    "AgentSpecification", 
] 