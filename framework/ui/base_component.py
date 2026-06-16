"""
BaseComponent — string-keyed element registry with fill/click/expect helpers.

All UI components and page objects inherit from this class.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.sync_api import Locator, Page

log = logging.getLogger(__name__)


class BaseComponent:
    """
    Provides a string-keyed ``element_name_mapping`` registry and wrappers
    around Playwright's auto-waiting element interactions.

    Subclasses populate ``element_name_mapping`` in ``__init__``::

        self.element_name_mapping.update({
            "Username": self.username_field,
            "Password": self.password_field,
        })

    Then tests use human-readable names::

        login_page.fill("Username", "admin@example.com")
        login_page.click("Login Button")
    """

    def __init__(self, page: "Page") -> None:
        self.page = page
        self.element_name_mapping: dict[str, "Locator"] = {}

    # ── Element resolution ────────────────────────────────────────────────────

    def _get_element(self, name: str) -> "Locator":
        if name not in self.element_name_mapping:
            raise KeyError(
                f"Element '{name}' not found in element_name_mapping. "
                f"Available: {list(self.element_name_mapping)}"
            )
        return self.element_name_mapping[name]

    # ── Interaction helpers ───────────────────────────────────────────────────

    def fill(self, element_name: str, value: str) -> None:
        log.debug("fill('%s')", element_name)
        self._get_element(element_name).fill(value)

    def click(self, element_name: str) -> None:
        log.debug("click('%s')", element_name)
        self._get_element(element_name).click()

    def clear(self, element_name: str) -> None:
        self._get_element(element_name).clear()

    def get_text(self, element_name: str) -> str:
        return self._get_element(element_name).inner_text()

    def get_value(self, element_name: str) -> str:
        return self._get_element(element_name).input_value()

    def is_visible(self, element_name: str) -> bool:
        return self._get_element(element_name).is_visible()

    def is_enabled(self, element_name: str) -> bool:
        return self._get_element(element_name).is_enabled()

    def select_option(self, element_name: str, value: str) -> None:
        self._get_element(element_name).select_option(value)

    def check(self, element_name: str) -> None:
        self._get_element(element_name).check()

    def uncheck(self, element_name: str) -> None:
        self._get_element(element_name).uncheck()

    # ── Wait helpers ──────────────────────────────────────────────────────────

    def wait_for_visible(self, element_name: str, timeout: int = 10_000) -> None:
        self._get_element(element_name).wait_for(state="visible", timeout=timeout)

    def wait_for_hidden(self, element_name: str, timeout: int = 10_000) -> None:
        self._get_element(element_name).wait_for(state="hidden", timeout=timeout)

    def wait_for_enabled(self, element_name: str, timeout: int = 10_000) -> None:
        self._get_element(element_name).wait_for(state="visible", timeout=timeout)

    # ── Playwright assertion wrappers ─────────────────────────────────────────

    def expect_visible(self, element_name: str) -> None:
        from playwright.sync_api import expect
        expect(self._get_element(element_name)).to_be_visible()

    def expect_hidden(self, element_name: str) -> None:
        from playwright.sync_api import expect
        expect(self._get_element(element_name)).to_be_hidden()

    def expect_text(self, element_name: str, expected: str) -> None:
        from playwright.sync_api import expect
        expect(self._get_element(element_name)).to_have_text(expected)

    def expect_value(self, element_name: str, expected: str) -> None:
        from playwright.sync_api import expect
        expect(self._get_element(element_name)).to_have_value(expected)

    def expect_enabled(self, element_name: str) -> None:
        from playwright.sync_api import expect
        expect(self._get_element(element_name)).to_be_enabled()

    # ── Progress bar / loading indicator waiter ───────────────────────────────

    def wait_for_progress_bar(self, timeout: int = 30_000) -> None:
        """
        Wait for any loading skeleton / progress bar to disappear.
        Best-effort: silently skips if the indicator is never found.
        """
        selectors = [
            '[role="progressbar"]',
            ".MuiSkeleton-root",
            ".loading-overlay",
            ".MuiCircularProgress-root",
        ]
        for selector in selectors:
            try:
                locator = self.page.locator(selector).first
                if locator.is_visible():
                    locator.wait_for(state="hidden", timeout=timeout)
            except Exception:  # noqa: BLE001
                pass
