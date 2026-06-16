"""String utility functions."""

from __future__ import annotations

import json
import logging
import re
from enum import Enum
from typing import Any

log = logging.getLogger(__name__)


class Format(Enum):
    alphabet = "alphabet"
    alphanumeric = "alphanumeric"
    boolean = "boolean"
    email = "email"
    url = "url"
    json = "json"
    integer = "integer"
    float_ = "float"
    list_ = "list"


def parse(string_input: str, expected_format: Format) -> Any:
    """Convert *string_input* to the Python type described by *expected_format*."""
    s = string_input.strip()
    if expected_format == Format.boolean:
        return s.lower() in ("true", "yes", "1")
    if expected_format == Format.integer:
        return int(s)
    if expected_format == Format.float_:
        return float(s)
    if expected_format == Format.json:
        return json.loads(s)
    if expected_format == Format.list_:
        return (
            json.loads(s)
            if s.startswith("[")
            else [item.strip() for item in s.split(",")]
        )
    return s


def get_api_url(url: str) -> str:
    """Return *url* stripped of trailing slashes."""
    return url.rstrip("/")


def format_elapsed_time(seconds: float) -> str:
    """Human-readable elapsed time: '1m 23s' or '45.1s'."""
    if seconds >= 60:
        return f"{int(seconds // 60)}m {int(seconds % 60)}s"
    return f"{seconds:.1f}s"


def trim_exception_message(exc: Exception, max_len: int = 200) -> str:
    """Return a truncated single-line exception message."""
    msg = str(exc).replace("\n", " ")
    return msg[:max_len] + "..." if len(msg) > max_len else msg
