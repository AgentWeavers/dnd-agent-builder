import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from agents import set_default_openai_api

from src.api.routers.chat import router as chat_router
from src.api.utils.logging import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting AgentWeaver application...")
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not set; please define it in your .env file")
    else:
        set_default_openai_api(api_key)
        logger.info("OpenAI API key configured")
    
    logger.info("AgentWeaver startup complete")
    
    yield
    
    logger.info("AgentWeaver shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="AgentWeaver",
    description="AI Agent API with dedicated endpoints per agent",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware for browser compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)         # /chat/* endpoints

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to AgentWeaver - AI Agent API",
        "version": "1.0.0",
        "architecture": "Dedicated routers per agent",
        "features": [
            "Per-agent dedicated endpoints",
            "Synchronous and streaming execution",
            "Standardized API patterns",
            "Real-time Server-Sent Events",
            "Simple and scalable"
        ],
        "api_docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "agents": ["research", "assistant", "coder"],
        "total_agents": 3
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting AgentWeaver with uvicorn...")
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
