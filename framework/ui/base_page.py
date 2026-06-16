"""BasePage — root class for all Page Object Models."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from framework.ui.base_component import BaseComponent

if TYPE_CHECKING:
    from playwright.sync_api import Page

log = logging.getLogger(__name__)


class BasePage(BaseComponent):
    """
    Base class for application page objects.

    Responsibilities:
    - navigate() / reload()
    - breadcrumb helpers
    - page-level Playwright assertions
    """

    def __init__(self, page: "Page", base_url: str) -> None:
        super().__init__(page)
        self._base_url = base_url.rstrip("/")

    # ── Navigation ────────────────────────────────────────────────────────────

    def navigate(self, path: str = "") -> "BasePage":
        """Navigate to ``base_url + path``."""
        url = f"{self._base_url}{path}"
        log.debug("Navigating to: %s", url)
        self.page.goto(url, wait_until="domcontentloaded")
        return self

    def reload(self) -> "BasePage":
        self.page.reload(wait_until="domcontentloaded")
        return self

    @property
    def current_url(self) -> str:
        return self.page.url

    @property
    def title(self) -> str:
        return self.page.title()

    # ── Breadcrumbs ───────────────────────────────────────────────────────────

    def get_breadcrumbs(self) -> list[str]:
        """Return breadcrumb text items from the page header."""
        crumbs = self.page.locator(
            '[aria-label="breadcrumb"] li, nav[aria-label="breadcrumb"] a'
        )
        return [c.inner_text().strip() for c in crumbs.all()]

    # ── Page-level assertions ─────────────────────────────────────────────────

    def wait_for_url(self, expected_pattern: str, timeout: int = 15_000) -> None:
        from playwright.sync_api import expect
        expect(self.page).to_have_url(expected_pattern, timeout=timeout)

    def wait_for_title(self, expected: str, timeout: int = 15_000) -> None:
        from playwright.sync_api import expect
        expect(self.page).to_have_title(expected, timeout=timeout)

    def wait_for_load(self, timeout: int = 30_000) -> "BasePage":
        """Wait for ``domcontentloaded`` and loading indicators to clear."""
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
        self.wait_for_progress_bar(timeout=timeout)
        return self
