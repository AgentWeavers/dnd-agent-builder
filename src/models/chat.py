from sqlmodel import SQLModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from sqlalchemy import JSON, Column
from sqlalchemy.types import DateTime

class Chat(SQLModel, table=True):
    __tablename__ = "chats"
    
    # Primary key is user_id from Stack Auth
    user_id: str = Field(primary_key=True, index=True)
    
    # Chat session identifier
    chat_id: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True)
    
    # Conversation data stored as JSONB
    conversation: Optional[Dict[str, Any]] = Field(
        default=None, 
        sa_type=JSON
    )
    
    # Metadata
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    
    # Optional fields for chat management
    title: Optional[str] = Field(default=None, index=True)
    is_active: bool = Field(default=True)
