#!/usr/bin/env python3
"""
ci_cd/log_pipeline.py
=====================
Structured logging infrastructure for AllBots.com.ai CI/CD pipelines.

Configures root logging to emit JSON-formatted records to both stdout and a
rotating log file.  Import this module at the start of any pipeline step to
ensure consistent, machine-parseable log output.

Usage (standalone)
------------------
    python ci_cd/log_pipeline.py
"""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler


LOG_FILE = "pipeline.log"
MAX_BYTES = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3


class _JsonFormatter(logging.Formatter):
    """Emit each log record as a single-line JSON object."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def configure_logging(level: int = logging.INFO) -> None:
    """Set up JSON logging on the root logger."""
    formatter = _JsonFormatter()

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    file_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(stream_handler)
    root.addHandler(file_handler)


if __name__ == "__main__":
    configure_logging()
    logger = logging.getLogger("pipeline")
    logger.info("Logging pipeline initialized.")
    logger.info("Pipeline run started.", extra={})
    logger.info("Pipeline run complete.")
