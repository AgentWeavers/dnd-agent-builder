import logging
import structlog
from src.core.config import settings

def configure_logging():
    # Configure structlog processors
    shared_processors = [
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # Configure the standard library logging to use structlog
    logging.basicConfig(
        format="%(message)s",
        level=settings.log_level,
        handlers=[
            logging.StreamHandler()
        ],
    )

    if settings.log_format == "console":
        renderer = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()
    
    # Setup structlog
    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Add structlog's formatter to the root logger
    formatter = structlog.stdlib.ProcessorFormatter(processor=renderer)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear() # Clear existing handlers to avoid duplicates
    root_logger.addHandler(handler)
    root_logger.setLevel(settings.log_level)