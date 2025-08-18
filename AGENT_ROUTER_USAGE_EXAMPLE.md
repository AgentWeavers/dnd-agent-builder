# Agent Router Usage Example with PostgreSQL Sessions

This document shows how to use the updated agent router that now integrates with your PostgreSQL `DatabaseSession` implementation.

## Basic Setup

### 1. Import Required Dependencies

```python
from fastapi import FastAPI, Depends
from src.api.utils.agent_router import create_agent_router
from src.dependencies.database import get_session
from agents import Agent
```

### 2. Create Your Agent

```python
# Create your OpenAI Agent
my_agent = Agent(
    name="DND Assistant",
    instructions="You are a helpful D&D campaign assistant. Help users with campaign planning, character creation, and game mechanics.",
    model="gpt-4o-mini"  # or your preferred model
)
```

### 3. Create the Router with Database Session Dependency

```python
# Create the router with database session dependency
agent_router = create_agent_router(
    agent=my_agent,
    prefix="/dnd-assistant",
    agent_name="DND Assistant",
    get_db_session=get_session  # Inject the database session dependency
)
```

### 4. Include in FastAPI App

```python
app = FastAPI(title="DND Agent Builder")

# Include the agent router
app.include_router(agent_router)

# Your other routers...
app.include_router(chat_storage_router)
```

## API Endpoints

The router automatically creates these endpoints:

- **POST** `/dnd-assistant/run` - Run the agent with session memory
- **POST** `/dnd-assistant/stream` - Stream agent responses with session memory
- **GET** `/dnd-assistant/info` - Get agent information

**Note**: Session management (viewing/clearing conversation history) is handled by the chat storage router (`/chats` endpoints) for better separation of concerns.

## Using Session Memory

### 1. Start a New Conversation

```bash
# Create a new chat first (using your chat storage API)
POST /chats/
{
    "title": "D&D Campaign Planning Session"
}

# Response will include chat_id
{
    "chat_id": "uuid-here",
    "user_id": "user123",
    "title": "D&D Campaign Planning Session",
    ...
}
```

### 2. Use the Agent with Session Memory

```bash
# First interaction - agent will start fresh
POST /dnd-assistant/run
{
    "input": "Help me create a fantasy campaign setting",
    "session_id": "uuid-here"
}

# Response will include the agent's output
{
    "final_output": "I'd be happy to help you create a fantasy campaign setting...",
    "success": true,
    "session_id": "uuid-here"
}
```

### 3. Continue the Conversation

```bash
# Second interaction - agent remembers previous context
POST /dnd-assistant/run
{
    "input": "What about the main villain?",
    "session_id": "uuid-here"
}

# The agent will automatically remember the campaign setting discussion
# and provide contextually relevant information about villains
```

### 4. Stream with Session Memory

```bash
# Streaming also maintains session memory
POST /dnd-assistant/stream
{
    "input": "Tell me about the geography of this world",
    "session_id": "uuid-here"
}

# You'll receive streaming events with full context
# The agent remembers all previous interactions
```

## Session Management

### 1. View Session History

```bash
# Get all messages in a session using the chat storage API
GET /chats/uuid-here

# Response shows conversation history
{
    "chat_id": "uuid-here",
    "user_id": "user123",
    "conversation": [
        {"role": "user", "content": "Help me create a fantasy campaign setting"},
        {"role": "assistant", "content": "I'd be happy to help..."},
        {"role": "user", "content": "What about the main villain?"},
        {"role": "assistant", "content": "For a fantasy campaign..."}
    ],
    "title": "D&D Campaign Planning Session",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:30:00Z"
}
```

### 2. Clear Session

```bash
# Clear conversation history by updating the chat
PUT /chats/uuid-here
{
    "conversation": null
}

# Or delete the chat entirely
DELETE /chats/uuid-here
```

### 3. Get Agent Information

```bash
# Get comprehensive agent info including session configuration
GET /dnd-assistant/info

# Response includes session type and configuration
{
    "name": "DND Assistant",
    "agent_name": "DND Assistant",
    "instructions": "You are a helpful D&D campaign assistant...",
    "model": "gpt-4o-mini",
    "tools_count": 0,
    "handoffs_count": 0,
    "endpoints": {
        "run": "/dnd-assistant/run",
        "stream": "/dnd-assistant/stream",
        "info": "/dnd-assistant/info"
    },
    "session_config": {
        "sessions_enabled": true,
        "session_type": "PostgreSQL",
        "description": "Sessions are enabled by default with PostgreSQL storage"
    }
}
```

## Environment Configuration

### 1. Database Configuration

```bash
# Ensure your database is configured
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5433/dnd_agent_db
DATABASE_ECHO=true
```

**Note**: Sessions are enabled by default - no additional configuration needed!

## Advanced Usage

### 1. Multiple Agents with Shared Sessions

```python
# Create multiple specialized agents
dnd_agent = Agent(name="DND Assistant", instructions="...")
character_agent = Agent(name="Character Creator", instructions="...")
world_agent = Agent(name="World Builder", instructions="...")

# Create routers for each
dnd_router = create_agent_router(dnd_agent, "/dnd", "DND Assistant", get_session)
character_router = create_agent_router(character_agent, "/character", "Character Creator", get_session)
world_router = create_agent_router(world_agent, "/world", "World Builder", get_session)

# Include all routers
app.include_router(dnd_router)
app.include_router(character_router)
app.include_router(world_router)

# Users can use the same session_id across different agents
# Each agent will have access to the full conversation history
```

### 2. Custom Session Logic

```python
# You can also create sessions manually if needed
from src.agents.utils.sessions import DatabaseSession

async def custom_agent_run(chat_id: str, user_input: str, db_session: AsyncSession):
    # Create session manually
    session = DatabaseSession(chat_id, db_session)
    
    # Run agent with custom logic
    result = await Runner.run(
        my_agent,
        user_input,
        session=session
    )
    
    return result
```

## Benefits of the New Implementation

1. **Persistent Memory**: Conversation history is stored in PostgreSQL and persists across server restarts
2. **Multi-User Support**: Each user can have multiple independent chat sessions
3. **Automatic Context**: Agents automatically have access to full conversation history
4. **Scalable Storage**: PostgreSQL handles large conversation histories efficiently
5. **Real-time Updates**: Session data is updated immediately after each interaction
6. **Streaming Support**: Full streaming support with maintained context
7. **Error Handling**: Robust error handling and logging throughout
8. **Protocol Compliance**: Fully compliant with OpenAI Agents SDK Session protocol
9. **Always Enabled**: Sessions work out of the box - no configuration needed
10. **Clean Separation**: Agent execution and conversation management are properly separated

## Architecture Benefits

### Separation of Concerns
- **Agent Router** (`/chat`): Handles agent execution and streaming
- **Chat Storage Router** (`/chats`): Handles conversation CRUD operations
- **No Duplication**: Each router has a clear, single responsibility

### Simplified Agent Router
- Focuses only on agent execution
- Removes redundant session management endpoints
- Cleaner, more maintainable code

### Unified Conversation Management
- All conversation operations go through `/chats` endpoints
- Consistent API for chat management
- Better for frontend integration

## Troubleshooting

### 1. Sessions Not Working

- Verify database connection is working
- Check logs for session creation errors
- Ensure the chat exists in the database

### 2. Database Errors

- Ensure PostgreSQL is running
- Check `DATABASE_URL` configuration
- Verify database tables exist (they're created automatically on startup)

### 3. Session Memory Issues

- Verify `session_id` is being passed correctly
- Check that the chat exists in the database
- Review logs for session loading errors

## Next Steps

1. **Test the Integration**: Try creating a chat and running an agent with session memory
2. **Monitor Performance**: Watch database performance with multiple concurrent sessions
3. **Add Monitoring**: Consider adding metrics for session usage and performance
4. **Scale Up**: Test with multiple agents and high session volumes

## Key Changes from Previous Version

- **Sessions are always enabled** - no environment variable configuration needed
- **Simplified setup** - just provide the database session dependency
- **Cleaner code** - removed unnecessary session enabling checks
- **Better performance** - no conditional logic for session creation
- **Cleaner separation** - agent router focuses on execution, chat storage handles conversation management
- **No duplicate endpoints** - session management consolidated in chat storage router
