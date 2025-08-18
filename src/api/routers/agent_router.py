from fastapi import APIRouter

from src.api.utils.agent_router import create_agent_router
from src.dependencies.database import get_session
from src.agent import planner_supervisor_agent


router = APIRouter()

router = create_agent_router(
    agent=planner_supervisor_agent,
    prefix="/agent",
    agent_name="Agent",
    get_db_session=get_session
)