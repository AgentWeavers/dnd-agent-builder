from agents.memory import Session
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.models.chat import Chat
import json
import structlog
from datetime import datetime, timezone
import uuid


def is_valid_uuid(uuid_string: str) -> bool:
    """
    Validate if a string is a valid UUID format.
    
    Args:
        uuid_string: String to validate
        
    Returns:
        bool: True if valid UUID format, False otherwise
    """
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False


logger = structlog.get_logger()

class DatabaseSession:
    """
    Custom session implementation that stores conversation history in PostgreSQL.
    Follows the OpenAI Agents SDK Session protocol.
    """
    
    def __init__(self, chat_id: str, db_session: AsyncSession, user_id: Optional[str] = None):
        """
        Initialize database session.
        
        Args:
            chat_id: Unique chat identifier
            db_session: SQLAlchemy async session for database operations
            user_id: Optional user ID for auto-creating chats when they don't exist
        """
        if not is_valid_uuid(chat_id):
            raise ValueError(f"Invalid UUID format: {chat_id}")
            
        self.chat_id = chat_id
        self.db_session = db_session
        self.user_id = user_id
        self._conversation_history: List[dict] = []
        self._loaded = False
    
    async def _load_conversation_history(self) -> None:
        """Load conversation history from database if not already loaded."""
        if self._loaded:
            return
            
        try:
            # Query by chat_id
            statement = select(Chat).where(Chat.chat_id == self.chat_id)
            result = await self.db_session.execute(statement)
            chat = result.scalars().first()
            
            if chat and chat.conversation:
                # Load existing conversation from database
                if isinstance(chat.conversation, str):
                    self._conversation_history = json.loads(chat.conversation)
                else:
                    self._conversation_history = chat.conversation
            else:
                # Start with empty history if no existing conversation
                self._conversation_history = []
                
            self._loaded = True
            logger.debug("Loaded conversation history", 
                        chat_id=self.chat_id, 
                        items_count=len(self._conversation_history))
            
        except Exception as e:
            logger.error("Failed to load conversation history", 
                        error=str(e), chat_id=self.chat_id)
            self._conversation_history = []
            self._loaded = True
    
    async def get_items(self, limit: Optional[int] = None) -> List[dict]:
        """
        Retrieve conversation history for this session.
        
        Args:
            limit: Maximum number of items to return (None for all)
            
        Returns:
            List of conversation items
        """
        await self._load_conversation_history()
        
        if limit is None:
            return self._conversation_history.copy()
        else:
            return self._conversation_history[-limit:].copy()
    
    async def add_items(self, items: List[dict]) -> None:
        """
        Store new items for this session.
        
        Args:
            items: List of conversation items to add
        """
        await self._load_conversation_history()
        
        # Add new items to memory
        self._conversation_history.extend(items)
        
        # Save to database
        await self._save_to_database()
    
    async def pop_item(self) -> Optional[dict]:
        """
        Remove and return the most recent item from this session.
        
        Returns:
            The most recent conversation item or None if empty
        """
        await self._load_conversation_history()
        
        if not self._conversation_history:
            return None
            
        item = self._conversation_history.pop()
        
        # Save updated history to database
        await self._save_to_database()
        
        return item
    
    async def clear_session(self) -> None:
        """Clear all items for this session."""
        self._conversation_history = []
        self._loaded = True
        
        # Clear from database
        await self._save_to_database(clear=True)
    
    async def _save_to_database(self, clear: bool = False) -> None:
        """Save current conversation history to database."""
        try:
            statement = select(Chat).where(Chat.chat_id == self.chat_id)
            result = await self.db_session.execute(statement)
            chat = result.scalars().first()
            
            if chat:
                # Update existing chat
                if clear:
                    chat.conversation = None
                else:
                    chat.conversation = self._conversation_history
                chat.updated_at = datetime.now(timezone.utc)
                await self.db_session.commit()
                logger.debug("Updated conversation history", 
                           chat_id=self.chat_id, 
                           items_count=len(self._conversation_history))
            else:
                # Chat doesn't exist - try to create it if we have user_id
                if self.user_id:
                    try:
                        # Create new chat with the provided chat_id
                        new_chat = Chat(
                            chat_id=self.chat_id,  # Use the provided UUID
                            user_id=self.user_id,
                            title=f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                            conversation=None if clear else self._conversation_history,
                            is_active=True,
                            created_at=datetime.now(timezone.utc),
                            updated_at=datetime.now(timezone.utc)
                        )
                        
                        self.db_session.add(new_chat)
                        await self.db_session.commit()
                        
                        logger.info("Auto-created new chat for user", 
                                  chat_id=self.chat_id, 
                                  user_id=self.user_id,
                                  items_count=len(self._conversation_history))
                    except Exception as create_error:
                        logger.error("Failed to auto-create chat", 
                                   error=str(create_error), 
                                   chat_id=self.chat_id, 
                                   user_id=self.user_id)
                        await self.db_session.rollback()
                        raise
                else:
                    logger.warning("No chat record found for conversation storage and no user_id provided for auto-creation", 
                                 chat_id=self.chat_id)
                
        except Exception as e:
            logger.error("Failed to save conversation history", 
                        error=str(e), chat_id=self.chat_id)
            await self.db_session.rollback()
            raise
