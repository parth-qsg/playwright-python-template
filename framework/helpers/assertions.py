"""Soft-assertion collector and screenshot-on-fail helpers."""

from __future__ import annotations

import json
import logging
import time
from typing import TYPE_CHECKING

from framework.exceptions import AssertionCollectionError

if TYPE_CHECKING:
    from playwright.sync_api import Page

log = logging.getLogger(__name__)


class SoftAssertions:
    """
    Collects assertion failures and reports them all at test end.

    Usage::

        soft = SoftAssertions()
        soft.check(response["status_code"] == 200, "Expected HTTP 200")
        soft.check("id" in response, "Response missing 'id'")
        soft.assert_all()   # raises AssertionCollectionError if any failed
    """

    def __init__(self) -> None:
        self._failures: list[str] = []

    def check(self, condition: bool, message: str) -> None:
        if not condition:
            log.debug("Soft-assert failed: %s", message)
            self._failures.append(message)

    def assert_all(self) -> None:
        if self._failures:
            summary = "\n  ".join(self._failures)
            raise AssertionCollectionError(
                f"{len(self._failures)} soft assertion(s) failed:\n  {summary}"
            )

    @property
    def has_failures(self) -> bool:
        return bool(self._failures)


# ── API response helpers ──────────────────────────────────────────────────────


def assert_status(response: dict, expected: int, message: str = "") -> None:
    actual = response.get("status_code")
    assert actual == expected, (
        message
        or f"Expected HTTP {expected}, got {actual}. "
        f"Body: {response.get('text', '')[:500]}"
    )


def assert_json_contains(response: dict, expected_keys: list[str]) -> None:
    try:
        body = json.loads(response.get("text", "{}"))
    except ValueError:
        body = {}
    missing = [k for k in expected_keys if k not in body]
    assert not missing, f"Response JSON missing keys: {missing}"


def assert_paginated_result(result: list, min_count: int = 1) -> None:
    assert isinstance(result, list), f"Expected list, got {type(result)}"
    assert len(result) >= min_count, (
        f"Expected ≥{min_count} item(s), got {len(result)}"
    )
