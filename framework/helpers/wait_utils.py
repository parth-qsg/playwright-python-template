"""Polling and wait utilities for non-UI conditions."""

from __future__ import annotations

import logging
import time
from typing import Any, Callable

from framework.exceptions import WaitTimeoutError

log = logging.getLogger(__name__)


def poll_until(
    condition_fn: Callable[[], Any],
    timeout_sec: float = 30,
    interval_sec: float = 1,
    error_msg: str = "",
) -> Any:
    """
    Repeatedly call *condition_fn* until it returns a truthy value.

    Returns the truthy return value.  Raises ``WaitTimeoutError`` on timeout.
    Exceptions raised by *condition_fn* are swallowed and retried.
    """
    deadline = time.monotonic() + timeout_sec
    last_exc: Exception | None = None
    while time.monotonic() < deadline:
        try:
            result = condition_fn()
            if result:
                return result
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            log.debug("poll_until swallowed: %s", exc)
        time.sleep(interval_sec)

    msg = error_msg or f"Condition not met within {timeout_sec}s"
    if last_exc:
        msg += f" (last exception: {last_exc})"
    raise WaitTimeoutError(msg)


def wait_for_http_status(
    api_fn: Callable[[], dict],
    expected_status: int,
    timeout_sec: float = 30,
    interval_sec: float = 2,
) -> dict:
    """
    Call *api_fn* repeatedly until its response dict carries the expected HTTP status.

    Returns the final response dict.
    """

    def _check() -> dict | None:
        resp = api_fn()
        return resp if resp.get("status_code") == expected_status else None

    return poll_until(
        _check,
        timeout_sec=timeout_sec,
        interval_sec=interval_sec,
        error_msg=f"HTTP {expected_status} not received within {timeout_sec}s",
    )
