"""UIContext — test hub for UI tests providing page access and PageFactory."""

from __future__ import annotations
import logging
import time
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.sync_api import Page
    from framework.ui.base_page import BasePage

log = logging.getLogger(__name__)


class UIContext:
    """Test hub for browser UI tests."""

    def __init__(self, page, base_url: str, screenshot_location: str = "results/screenshots") -> None:
        self.page = page
        self._base_url = base_url
        self._screenshot_location = screenshot_location
        Path(screenshot_location).mkdir(parents=True, exist_ok=True)

    def page_factory(self, page_type: str):
        """Return a page-object instance by its registered string key."""
        from framework.ui.page_factory import PageFactory
        return PageFactory.create(page_type, self.page, self._base_url)

    def screenshot(self, name: str) -> str:
        """Take a screenshot; return the saved file path."""
        ts = int(time.time())
        safe = name.replace(" ", "_").replace("/", "_")[:80]
        path = f"{self._screenshot_location}/{safe}_{ts}.png"
        try:
            self.page.screenshot(path=path)
            log.info("Screenshot: %s", path)
        except Exception as exc:  # noqa: BLE001
            log.warning("Screenshot failed: %s", exc)
        return path

    def verify(self, condition_fn: object, error_msg: str = "") -> None:
        """Soft-assert: evaluate condition_fn, screenshot + raise on failure."""
        try:
            result = condition_fn() if callable(condition_fn) else condition_fn
            if not result:
                raise AssertionError(error_msg or "Condition returned falsy")
        except Exception as exc:
            self.screenshot(f"verify_fail_{str(error_msg)[:40]}")
            raise AssertionError(f"verify() failed: {exc}") from exc
