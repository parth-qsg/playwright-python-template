"""UI test fixtures: browser_context_args, ui_context."""

from __future__ import annotations

from typing import Generator

import pytest

from framework.contexts.ui_context import UIContext
from framework.configuration.config import Configuration

# Import all page modules to trigger PageFactory.register() calls
import pages  # noqa: F401


@pytest.fixture(scope="session")
def browser_context_args(config) -> dict:
    """Session-scoped Playwright browser context arguments (viewport, https)."""
    viewport_cfg = config.ui_viewport
    size_key = viewport_cfg.get("default", "hd")
    viewport = viewport_cfg.get(size_key, {"width": 1920, "height": 1080})
    return {
        "viewport": viewport,
        "ignore_https_errors": True,
    }


@pytest.fixture
def ui_context(
    page, base_url, config
) -> Generator[UIContext, None, None]:
    """Function-scoped UI context wrapping the Playwright page."""
    ctx = UIContext(
        page=page,
        base_url=base_url,
        screenshot_location=config.screenshot_location,
    )
    yield ctx
