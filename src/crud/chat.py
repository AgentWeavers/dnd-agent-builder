from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update
from datetime import datetime, timezone
import structlog

from src.models.chat import Chat
from src.schemas.chat import ChatCreate, ChatUpdate

logger = structlog.get_logger()

async def create_chat(session: AsyncSession, user_id: str, chat_data: ChatCreate) -> Chat:
    """Create a new chat for a user."""
    chat = Chat(
        user_id=user_id,
        title=chat_data.title,
        conversation=chat_data.conversation,
        is_active=chat_data.is_active
    )
    
    session.add(chat)
    await session.commit()
    await session.refresh(chat)
    
    logger.info("Created chat", chat_id=chat.chat_id, user_id=user_id)
    return chat

async def create_new_chat_for_user(session: AsyncSession, user_id: str, title: Optional[str] = None) -> str:
    """Create a new chat for a user and return the chat_id for use with DatabaseSession."""
    chat = Chat(
        user_id=user_id,
        title=title or f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        conversation=None,
        is_active=True
    )
    
    session.add(chat)
    await session.commit()
    await session.refresh(chat)
    
    logger.info("Created new chat for user", chat_id=chat.chat_id, user_id=user_id)
    return chat.chat_id

async def get_chat_by_id(session: AsyncSession, chat_id: str, user_id: str) -> Optional[Chat]:
    """Get a specific chat by ID for a user."""
    statement = select(Chat).where(
        Chat.chat_id == chat_id,
        Chat.user_id == user_id
    )
    result = await session.execute(statement)
    return result.scalars().first()

async def get_user_chats(
    session: AsyncSession, 
    user_id: str, 
    skip: int = 0, 
    limit: int = 100,
    active_only: bool = True
) -> List[Chat]:
    """Get all chats for a user with pagination."""
    statement = select(Chat).where(Chat.user_id == user_id)
    
    if active_only:
        statement = statement.where(Chat.is_active == True)
    
    statement = statement.order_by(Chat.updated_at.desc()).offset(skip).limit(limit)
    
    result = await session.execute(statement)
    return result.scalars().all()

async def update_chat(
    session: AsyncSession, 
    chat_id: str, 
    user_id: str,
    chat_data: ChatUpdate
) -> Optional[Chat]:
    """Update an existing chat."""
    chat = await get_chat_by_id(session, chat_id, user_id)
    if not chat:
        return None
    
    # Update fields if provided
    update_data = chat_data.model_dump(exclude_unset=True)
    if update_data:
        update_data['updated_at'] = datetime.now(timezone.utc)
        
        statement = (
            update(Chat)
            .where(
                Chat.chat_id == chat_id,
                Chat.user_id == user_id
            )
            .values(**update_data)
        )
        await session.execute(statement)
        await session.commit()
        await session.refresh(chat)
        
        logger.info("Updated chat", chat_id=chat_id, user_id=user_id)
    
    return chat

async def delete_chat(session: AsyncSession, chat_id: str, user_id: str) -> bool:
    """Delete a chat (soft delete by setting is_active to False)."""
    chat = await get_chat_by_id(session, chat_id, user_id)
    if not chat:
        return False
    
    chat.is_active = False
    chat.updated_at = datetime.now(timezone.utc)
    
    await session.commit()
    logger.info("Deleted chat", chat_id=chat_id, user_id=user_id)
    return True

async def hard_delete_chat(session: AsyncSession, chat_id: str, user_id: str) -> bool:
    """Permanently delete a chat from the database."""
    chat = await get_chat_by_id(session, chat_id, user_id)
    if not chat:
        return False
    
    await session.delete(chat)
    await session.commit()
    
    logger.info("Hard deleted chat", chat_id=chat_id, user_id=user_id)
    return True

async def get_chat_count(session: AsyncSession, user_id: str, active_only: bool = True) -> int:
    """Get the total count of chats for a user."""
    statement = select(Chat).where(Chat.user_id == user_id)
    
    if active_only:
        statement = statement.where(Chat.is_active == True)
    
    result = await session.execute(statement)
    return len(result.scalars().all())
