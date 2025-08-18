from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import AsyncSessionLocal

async def get_session() -> AsyncSession:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        yield session
