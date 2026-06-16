"""pytest-html custom hooks: report title and environment table."""

from __future__ import annotations

import logging
import platform

log = logging.getLogger(__name__)


def pytest_html_report_title(report) -> None:
    """Set a custom title for the HTML report."""
    report.title = "Playwright Python — Automation Results"


def pytest_html_environment(config) -> dict:
    """Populate the Environment table in the HTML report."""
    from framework.configuration.config import Configuration

    if not Configuration.is_initialized():
        return {}

    return {
        "Base URL": Configuration.base_url,
        "Headless": str(Configuration.headless_mode),
        "Python": platform.python_version(),
        "Platform": platform.system(),
    }
