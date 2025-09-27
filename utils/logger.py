from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from .settings import load_settings


def configure_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    settings = load_settings()
    log_dir = Path(settings.app.artifacts_dir) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.setLevel(level)
    handler = logging.FileHandler(log_dir / f"{name}.log", encoding="utf-8")
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger


def redact_secrets(payload: dict[str, Any]) -> dict[str, Any]:
    redacted = {}
    for key, value in payload.items():
        if any(secret_key in key.lower() for secret_key in {"api_key", "password", "token"}):
            redacted[key] = "***redacted***"
        else:
            redacted[key] = value
    return redacted
