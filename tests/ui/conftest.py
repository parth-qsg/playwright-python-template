"""UI-layer conftest: screenshot-on-failure autouse fixture (UI tests only)."""

import logging

import pytest

from framework.configuration.config import Configuration

log = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page):
    """
    Autouse fixture for all tests under tests/ui/.
    Captures a screenshot whenever a test fails.
    Requires ``pytest_runtest_makereport`` in root conftest to populate
    ``request.node.rep_call``.
    """
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshot_dir = (
            Configuration.screenshot_location
            if Configuration.is_initialized()
            else "results/screenshots"
        )
        safe_name = request.node.name.replace("[", "_").replace("]", "_")
        path = f"{screenshot_dir}/FAIL_{safe_name}.png"
        try:
            page.screenshot(path=path)
            log.info("Failure screenshot saved: %s", path)
        except Exception as exc:  # noqa: BLE001
            log.warning("Could not save failure screenshot: %s", exc)
