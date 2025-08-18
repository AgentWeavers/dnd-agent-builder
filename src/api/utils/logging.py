import logging
import sys
import os
import structlog

def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Configures and returns a logger with a standard format.
    The logging level can be set via the LOG_LEVEL environment variable (e.g., INFO, DEBUG).
    """
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    # Configure structlog
    if not structlog.is_configured():
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                structlog.processors.JSONRenderer(),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    # Get the logger
    logger = structlog.get_logger(name)
    logger.setLevel(log_level)
    
    # Add a handler if not already present
    if not logging.getLogger(name).handlers:
        handler = logging.StreamHandler(sys.stdout)
        # No need to set a formatter for the handler, structlog handles it
        logging.getLogger(name).addHandler(handler)
        
    return logger
