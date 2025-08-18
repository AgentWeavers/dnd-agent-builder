from plistlib import load
from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings using pydantic-settings for validation"""
    
    # Stack Auth Configuration (official naming from docs)
    stack_project_id: str = os.getenv("STACK_PROJECT_ID", "")
    stack_publishable_client_key: str = os.getenv("STACK_PUBLISHABLE_CLIENT_KEY", "")
    stack_secret_server_key: str = os.getenv("STACK_SECRET_SERVER_KEY", "")
    stack_api_base_url: str = os.getenv("STACK_API_BASE_URL", "https://api.stack-auth.com")
    
    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "")
    
    # Application Configuration
    app_name: str = "DND Agent Builder API"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    enable_sessions: bool = os.getenv("ENABLE_SESSIONS", "False").lower() == "true"
    session_db_path: str = os.getenv("SESSION_DB_PATH", "")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    deep_research_search_api: str = os.getenv("DEEP_RESEARCH_SEARCH_API", "")
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_format: str = os.getenv("LOG_FORMAT", "console")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()