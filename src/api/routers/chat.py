from fastapi import APIRouter

from src.api.utils.logging import get_logger
from src.api.utils.agent_router import create_agent_router
from src.chat_orchestrator.agent import chat_agent

logger = get_logger(__name__)
router = APIRouter()

router = create_agent_router(
    agent=chat_agent,
    prefix="/chat",
    agent_name="Chat Agent"
)