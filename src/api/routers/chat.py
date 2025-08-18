from fastapi import APIRouter

from src.api.utils.agent_router import create_agent_router
from src.agent import planner_supervisor_agent


router = APIRouter()

router = create_agent_router(
    agent=planner_supervisor_agent,
    prefix="/chat",
    agent_name="Chat Agent"
)