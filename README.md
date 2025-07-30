# DnD Agent Builder Agent

An Agent which helps build you agents.

## Run it locally

- **[uv](https://github.com/astral-sh/uv)** - Fast Python package manager
- **OpenAI API Key** - Set in environment variables

## Installation & Setup

### 1. Install uv (if not already installed)

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Via pip
pip install uv
```

### 2. Clone and Setup Project

```bash
git clone https://github.com/AgentWeavers/dnd-agent-builder.git
cd dnd-agent-builder

# Create virtual environment with correct Python version
uv venv

# Activate virtual environment
# On Unix/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install project in development mode with all dependencies
uv pip install -e .
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```bash
# .env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key

# Session Memory Configuration (Optional)
ENABLE_SESSIONS=true                    # Enable conversation memory
SESSION_DB_PATH=./conversations.db      # SQLite database path

# Optional: Logging level
LOG_LEVEL=INFO

# Optional: Custom port (default is 8000)
PORT=8000
```

## Running the Application

### Development Mode (Recommended)

```bash
# Using uvicorn directly (with hot reload)
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Or using the module directly
python -m src.api.main
```
