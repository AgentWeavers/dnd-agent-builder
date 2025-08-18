from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies.auth import get_current_user
from src.dependencies.database import get_session
from src.schemas.chat import ChatCreate, ChatUpdate, ChatResponse, ChatListResponse
from src.crud.chat import (
    create_chat, get_chat_by_id, get_user_chats, update_chat, 
    delete_chat, get_chat_count
)
import structlog

logger = structlog.get_logger()

router = APIRouter(prefix="/chats", tags=["chats"])

@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_new_chat(
    chat_data: ChatCreate,
    user_data: Dict[str, Any] = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Create a new chat for the current user."""
    try:
        chat = await create_chat(session, user_data["user_id"], chat_data)
        return ChatResponse.model_validate(chat)
    except Exception as e:
        logger.error("Failed to create chat", error=str(e), user_id=user_data["user_id"])
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create chat"
        )

@router.get("/", response_model=ChatListResponse)
async def get_chats(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    user_data: Dict[str, Any] = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get all chats for the current user with pagination."""
    try:
        chats = await get_user_chats(session, user_data["user_id"], skip, limit, active_only)
        total = await get_chat_count(session, user_data["user_id"], active_only)
        
        return ChatListResponse(
            chats=[ChatResponse.model_validate(chat) for chat in chats],
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        logger.error("Failed to get chats", error=str(e), user_id=user_data["user_id"])
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get chats"
        )

@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: str,
    user_data: Dict[str, Any] = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get a specific chat by ID."""
    try:
        chat = await get_chat_by_id(session, user_data["user_id"], chat_id)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found"
            )
        
        return ChatResponse.model_validate(chat)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get chat", error=str(e), chat_id=chat_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get chat"
        )

@router.put("/{chat_id}", response_model=ChatResponse)
async def update_chat_details(
    chat_id: str,
    chat_data: ChatUpdate,
    user_data: Dict[str, Any] = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Update an existing chat."""
    try:
        chat = await update_chat(session, user_data["user_id"], chat_id, chat_data)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found"
            )
        
        return ChatResponse.model_validate(chat)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update chat", error=str(e), chat_id=chat_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update chat"
        )

@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_endpoint(
    chat_id: str,
    user_data: Dict[str, Any] = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Delete a chat (soft delete)."""
    try:
        success = await delete_chat(session, user_data["user_id"], chat_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete chat", error=str(e), chat_id=chat_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete chat"
        )
