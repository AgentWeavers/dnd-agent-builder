from sqlmodel import SQLModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from sqlalchemy import JSON, Column, Index
from sqlalchemy.types import DateTime

class Chat(SQLModel, table=True):
    __tablename__ = "chats"
    
    # Primary key should be chat_id for unique chats
    chat_id: str = Field(primary_key=True, default_factory=lambda: str(uuid.uuid4()), index=True)
    
    # Foreign key to user (not primary key)
    user_id: str = Field(index=True)  # Reference to Stack Auth user
    
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
        sa_column=Column(DateTime(timezone=True), nullable=False, onupdate=datetime.now(timezone.utc))
    )
    
    # Optional fields for chat management
    title: Optional[str] = Field(default=None, index=True)
    is_active: bool = Field(default=True)
