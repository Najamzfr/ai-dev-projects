"""Logging configuration."""
import logging
import sys
from app.config import settings


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record):
        """Format log record as JSON."""
        import json

        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Add extra fields
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "method"):
            log_data["method"] = record.method
        if hasattr(record, "path"):
            log_data["path"] = record.path
        if hasattr(record, "status_code"):
            log_data["status_code"] = record.status_code
        if hasattr(record, "process_time"):
            log_data["process_time"] = record.process_time
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging():
    """Configure application logging."""
    import logging

    # Get log level safely
    log_level_str = settings.log_level.upper()
    if log_level_str == "DEBUG":
        log_level = logging.DEBUG
    elif log_level_str == "INFO":
        log_level = logging.INFO
    elif log_level_str == "WARNING":
        log_level = logging.WARNING
    elif log_level_str == "ERROR":
        log_level = logging.ERROR
    else:
        log_level = logging.INFO

    if settings.log_format == "json":
        # JSON logging for production
        import logging.handlers

        formatter = JSONFormatter()
    else:
        # Text logging for development
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)

    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

