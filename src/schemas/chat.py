from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ChatBase(BaseModel):
    """Base chat schema with common fields."""
    title: Optional[str] = None
    conversation: Optional[Dict[str, Any]] = None
    is_active: bool = True

class ChatCreate(ChatBase):
    """Schema for creating a new chat."""
    pass

class ChatUpdate(BaseModel):
    """Schema for updating an existing chat."""
    title: Optional[str] = None
    conversation: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class ChatResponse(ChatBase):
    """Schema for chat responses."""
    user_id: str
    chat_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChatListResponse(BaseModel):
    """Schema for listing chats."""
    chats: list[ChatResponse]
    total: int
    skip: int
    limit: int
