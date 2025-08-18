FROM python:3.13-slim 
 
# Set environment variables 
ENV PYTHONDONTWRITEBYTECODE=1 \ 
    PYTHONUNBUFFERED=1 \ 
    PIP_NO_CACHE_DIR=1 
 
# Install uv globally
RUN pip install --no-cache-dir uv 
 
# Set the working directory 
WORKDIR /app 
 
# Copy dependency files 
COPY pyproject.toml uv.lock ./ 
 
# Install dependencies using uv (this will create a .venv in the project)
RUN uv sync --no-dev --no-cache --frozen 
 
# Copy the application code 
COPY . . 
 
EXPOSE 8000 
 
# Use uv to run the command (ensures proper venv activation)
CMD ["uv", "run", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]