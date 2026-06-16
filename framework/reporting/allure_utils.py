"""
Allure report utilities.

Gracefully degrades to no-ops when allure-pytest is not installed.
"""

from __future__ import annotations

import logging
from typing import Callable

log = logging.getLogger(__name__)

try:
    import allure as _allure

    ALLURE_AVAILABLE = True
except ImportError:
    _allure = None  # type: ignore[assignment]
    ALLURE_AVAILABLE = False


# ── Step decorator ────────────────────────────────────────────────────────────


def step(title: str) -> Callable:
    """Allure ``@step`` decorator. Returns a no-op decorator if Allure is absent."""
    if ALLURE_AVAILABLE:
        return _allure.step(title)

    def _noop(fn: Callable) -> Callable:
        return fn

    return _noop


# ── Attachments ───────────────────────────────────────────────────────────────


def attach_screenshot(screenshot_path: str, name: str = "Screenshot") -> None:
    """Attach a PNG screenshot to the Allure report."""
    if not ALLURE_AVAILABLE:
        log.debug("Allure not available; skipping screenshot attachment.")
        return
    try:
        with open(screenshot_path, "rb") as f:
            _allure.attach(
                f.read(),
                name=name,
                attachment_type=_allure.attachment_type.PNG,
            )
    except OSError as exc:
        log.warning("Could not attach screenshot to Allure: %s", exc)


def attach_response(response: dict, name: str = "API Response") -> None:
    """Attach an API response dict (status + body) to the Allure report."""
    import json

    body = json.dumps(
        {
            "status_code": response.get("status_code"),
            "text": response.get("text", ""),
        },
        indent=2,
    )
    if ALLURE_AVAILABLE:
        _allure.attach(
            body,
            name=name,
            attachment_type=_allure.attachment_type.JSON,
        )
    else:
        log.debug(
            "API Response [%s]: %s",
            response.get("status_code"),
            response.get("text", "")[:200],
        )
