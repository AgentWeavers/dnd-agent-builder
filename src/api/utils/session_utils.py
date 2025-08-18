"""
Simple session utilities for OpenAI Agents with PostgreSQL database integration.

This module provides a clean, minimal interface for session memory using PostgreSQL.
Sessions are enabled by default for all agent interactions.
"""

import logging
from typing import Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession

from agents.items import TResponseInputItem
from src.agents.utils.sessions import DatabaseSession

logger = logging.getLogger(__name__)

async def create_session_if_enabled(
    chat_id: Optional[str], 
    db_session: AsyncSession
) -> Optional[DatabaseSession]:
    """
    Create a PostgreSQL session if chat_id is provided.
    
    Args:
        chat_id: Optional chat identifier
        db_session: SQLAlchemy async session for database operations
        
    Returns:
        DatabaseSession if chat_id provided, None otherwise
    """
    if not chat_id:
        return None
    
    try:
        session = DatabaseSession(chat_id=chat_id, db_session=db_session)
        logger.info(f"Created PostgreSQL session: {chat_id}")
        return session
    except Exception as e:
        logger.error(f"Failed to create session {chat_id}: {e}")
        return None

async def get_session_messages(
    chat_id: str, 
    db_session: AsyncSession, 
    limit: Optional[int] = None
) -> Optional[List[dict]]:
    """
    Retrieve all messages for a session.
    
    Args:
        chat_id: Chat identifier to retrieve messages for
        db_session: SQLAlchemy async session
        limit: Optional limit on number of messages to retrieve (None for all)
        
    Returns:
        List of conversation items if successful, None if failed
    """
    try:
        session = DatabaseSession(chat_id=chat_id, db_session=db_session)
        messages = await session.get_items(limit=limit)
        logger.info(f"Retrieved {len(messages)} messages for session: {chat_id}")
        return messages
    except Exception as e:
        logger.error(f"Failed to retrieve messages for session {chat_id}: {e}")
        return None

async def clear_session(chat_id: str, db_session: AsyncSession) -> bool:
    """
    Clear a session's conversation history.
    
    Args:
        chat_id: Session to clear
        db_session: SQLAlchemy async session
        
    Returns:
        bool: True if cleared successfully, False otherwise
    """
    try:
        session = DatabaseSession(chat_id=chat_id, db_session=db_session)
        await session.clear_session()
        logger.info(f"Cleared session: {chat_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to clear session {chat_id}: {e}")
        return False

def get_session_info() -> dict:
    """
    Get current session configuration information.
    
    Returns:
        dict: Session configuration details
    """
    return {
        "sessions_enabled": True,
        "session_type": "PostgreSQL",
        "description": "Sessions are enabled by default with PostgreSQL storage"
    } 