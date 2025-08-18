# Chat Storage Implementation Summary

## Overview
This document summarizes the implementation of a database table for saving user agent chat conversations in the DND Agent Builder project.

## Architecture

### 1. Database Model (`src/models/chat.py`)
- **Table Name**: `chats`
- **Primary Key**: `chat_id` (UUID for unique chat identification)
- **User Reference**: `user_id` (indexed field from Stack Auth service)
- **Conversation Data**: `conversation` (JSONB field storing list of conversation messages)
- **Metadata**: `created_at`, `updated_at`, `title`, `is_active`
- **Indexes**: Optimized for user queries and active chat filtering

### 2. API Schemas (`src/schemas/chat.py`)
- **ChatBase**: Common fields for chat operations
- **ChatCreate**: Schema for creating new chats
- **ChatUpdate**: Schema for updating existing chats
- **ChatResponse**: Schema for API responses
- **ChatListResponse**: Schema for paginated chat lists

### 3. CRUD Operations (`src/crud/chat.py`)
- **create_chat**: Create new chat for user
- **create_new_chat_for_user**: Create chat and return chat_id for session use
- **get_chat_by_id**: Retrieve specific chat by ID
- **get_user_chats**: Get paginated list of user's chats
- **update_chat**: Update existing chat details
- **delete_chat**: Soft delete chat (sets is_active to False)
- **hard_delete_chat**: Permanently delete chat from database
- **get_chat_count**: Get total count of user's chats

### 4. API Endpoints (`src/api/routers/chat_storage.py`)
- **POST** `/chats/` - Create new chat
- **GET** `/chats/` - List user's chats with pagination
- **GET** `/chats/{chat_id}` - Get specific chat
- **PUT** `/chats/{chat_id}` - Update chat details
- **DELETE** `/chats/{chat_id}` - Delete chat (soft delete)

### 5. DatabaseSession Implementation (`src/agents/utils/sessions.py`)
- **Protocol Compliance**: Properly implements OpenAI Agents SDK Session protocol
- **Conversation Loading**: Loads existing conversation history from database
- **Persistent Storage**: Saves conversation updates to PostgreSQL
- **Error Handling**: Robust error handling with proper logging

### 6. Session Utilities (`src/api/utils/session_utils.py`)
- **PostgreSQL Integration**: Uses DatabaseSession instead of SQLiteSession
- **Async Support**: All functions are async and require database session
- **Always Enabled**: Sessions are enabled by default for all agent interactions
- **Session Management**: Create, retrieve, and clear session functionality

### 7. Agent Router Integration (`src/api/utils/agent_router.py`)
- **Database Session Dependency**: Injects database session into all agent endpoints
- **Automatic Session Creation**: Creates PostgreSQL sessions when session_id is provided
- **Session Memory**: Maintains conversation context across agent runs
- **Streaming Support**: Full streaming support with session memory
- **Focused Responsibility**: Handles only agent execution, not conversation management

## Key Features

### Authentication Integration
- Uses Stack Auth service for user authentication
- User ID is extracted from `get_current_user` dependency
- All operations are scoped to the authenticated user

### Data Storage
- **JSONB Field**: The `conversation` field stores chat data as JSON, allowing flexible conversation structure
- **Soft Deletes**: Chats are marked as inactive rather than permanently removed
- **Timestamps**: Automatic creation and update timestamps with timezone support
- **Auto-update**: `updated_at` field automatically updates on modifications

### Security & Access Control
- All endpoints require authentication
- Users can only access their own chats
- Chat operations are properly scoped by user_id

### Session Management
- **Proper Protocol Implementation**: Follows OpenAI Agents SDK Session protocol exactly
- **History Persistence**: Maintains conversation context across multiple agent runs
- **Automatic Loading**: Loads existing conversation history when session is initialized
- **Real-time Updates**: Saves conversation changes immediately to database

### Agent Integration
- **Seamless Integration**: Works directly with FastAPI agent endpoints
- **Automatic Context**: Agents automatically have access to conversation history
- **Streaming Support**: Full streaming support with maintained context
- **Session Lifecycle**: Automatic session creation, management, and cleanup

## Database Schema

```sql
CREATE TABLE chats (
    chat_id TEXT PRIMARY KEY,              -- Unique chat session ID
    user_id TEXT NOT NULL,                 -- Stack Auth user ID (indexed)
    conversation JSONB,                     -- Chat conversation data (list of messages)
    title TEXT,                            -- Optional chat title (indexed)
    is_active BOOLEAN DEFAULT TRUE,        -- Soft delete flag
    created_at TIMESTAMP WITH TIME ZONE,   -- Creation timestamp
    updated_at TIMESTAMP WITH TIME ZONE    -- Last update timestamp (auto-updates)
);

-- Indexes for efficient queries
CREATE INDEX idx_user_chats ON chats(user_id, created_at);
CREATE INDEX idx_active_chats ON chats(user_id, is_active);
```

## Integration Points

### FastAPI Application
- Router is included in `src/api/main.py`
- Database initialization includes Chat table creation
- Uses existing database connection and session management

### Dependencies
- **Database**: Uses `src/dependencies/database.py` for session management
- **Authentication**: Uses `src/dependencies/auth.py` for user verification
- **Logging**: Integrated with structlog for structured logging

### OpenAI Agents SDK Integration
- **Session Protocol**: Fully compliant with `agents.memory.Session` protocol
- **Automatic History**: Works seamlessly with `Runner.run(agent, input, session=session)`
- **Context Preservation**: Maintains conversation context across multiple agent executions

### Agent Router Integration
- **Database Session Injection**: All agent endpoints automatically receive database sessions
- **Session Creation**: Sessions are created automatically when session_id is provided
- **Memory Persistence**: Conversation history is maintained across multiple agent runs
- **Streaming Support**: Full streaming support with session memory intact

## Usage Examples

### Creating a New Chat and Session
```python
from src.crud.chat import create_new_chat_for_user
from src.agents.utils.sessions import DatabaseSession
from agents import Agent, Runner

# Create new chat
chat_id = await create_new_chat_for_user(db_session, "user_123", "My AI Assistant Chat")

# Create session for the agent
session = DatabaseSession(chat_id, db_session)

# Use with agent
result = await Runner.run(
    agent,
    "Hello, I need help with Python",
    session=session
)
```

### Using with FastAPI Agent Endpoints
```python
# The agent router automatically handles session creation
# POST /chat/run
{
    "input": "Hello, I need help with Python",
    "session_id": "chat_uuid_here"
}

# The agent will automatically:
# 1. Load existing conversation history from PostgreSQL
# 2. Run the agent with full context
# 3. Save new conversation items to the database
# 4. Maintain context for future requests
```

### Resuming Existing Chat
```python
# Session automatically loads existing conversation history
session = DatabaseSession(existing_chat_id, db_session)

# Agent will have full context from previous interactions
result = await Runner.run(
    agent,
    "What did we discuss earlier?",
    session=session
)
```

### Updating Chat Conversation
```python
PUT /chats/{chat_id}
{
    "conversation": [
        {"role": "user", "content": "Help me plan a D&D campaign"},
        {"role": "assistant", "content": "I'd be happy to help!"},
        {"role": "user", "content": "I want a fantasy setting"}
    ]
}
```

**Note**: The `conversation` field stores a list of message objects, where each message typically has:
- `role`: "user" or "assistant"
- `content`: The message text
- `type`: Message type (e.g., "message", "tool_call", etc.)
- Additional metadata as needed
```

## Key Improvements Made

1. **Fixed Primary Key**: `chat_id` is now the primary key, allowing proper unique chat identification
2. **Proper Session Protocol**: Implements the SDK's expected session behavior correctly
3. **Actual History Loading**: Loads existing conversation history instead of always starting empty
4. **Multi-User Support**: Schema supports multiple users with multiple chats each
5. **Future Extensibility**: Schema designed for easy expansion with related tables
6. **Error Handling**: Proper error handling and logging throughout
7. **Auto-updating Timestamps**: `updated_at` field automatically updates on modifications
8. **Optimized Indexes**: Database indexes for efficient user queries and filtering
9. **Agent Router Integration**: Seamless integration with FastAPI agent endpoints
10. **PostgreSQL Migration**: Replaced SQLite with robust PostgreSQL storage
11. **Clean Architecture**: Proper separation of concerns between agent execution and conversation management

## Architecture Benefits

### Separation of Concerns
- **Agent Router** (`/chat`): Handles agent execution and streaming only
- **Chat Storage Router** (`/chats`): Handles all conversation CRUD operations
- **No Duplication**: Each router has a clear, single responsibility

### Simplified Agent Router
- Focuses only on agent execution
- Removes redundant session management endpoints
- Cleaner, more maintainable code

### Unified Conversation Management
- All conversation operations go through `/chats` endpoints
- Consistent API for chat management
- Better for frontend integration

## Next Steps

1. **Database Setup**: Ensure PostgreSQL is running and accessible
2. **Environment Variables**: Set `DATABASE_URL` in `.env` file
3. **Testing**: Create comprehensive tests for all CRUD operations and session functionality
4. **Frontend Integration**: Connect frontend to chat storage endpoints
5. **Real-time Updates**: Consider adding WebSocket support for live chat updates
6. **Agent Deployment**: Deploy agents using the updated router with PostgreSQL sessions

## Dependencies Added
- `asyncpg`: PostgreSQL async driver
- `sqlmodel`: SQL database ORM
- `pydantic`: Data validation (already present)

## Notes
- No separate user table is needed as Stack Auth handles user management
- The implementation follows FastAPI best practices with proper error handling
- All database operations are asynchronous for better performance
- The JSONB field allows for flexible conversation structure without schema changes
- The DatabaseSession now properly follows the OpenAI Agents SDK Session protocol
- Conversation history is automatically loaded and persisted across agent runs
- The schema is optimized for multi-user, multi-chat scenarios
- The agent router automatically handles session creation and management
- Full streaming support is maintained with session memory intact
- Clean separation of concerns: agent execution vs. conversation management
- No duplicate endpoints between routers