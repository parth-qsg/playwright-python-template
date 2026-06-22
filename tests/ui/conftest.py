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


@pytest.fixture(autouse=True)
def attach_allure_artifacts(request, context, page):
    """
    Autouse fixture for all tests under tests/ui/.

    On test failure:
      1. Attaches a screenshot to the Allure report.
      2. Closes the browser context so the video file is finalised.
      3. Attaches the video to the Allure report.

    Requires ``pytest_runtest_makereport`` in root conftest to populate
    ``request.node.rep_call``.
    """
    yield

    if not (hasattr(request.node, "rep_call") and request.node.rep_call.failed):
        return

    # 1. Screenshot — page is still open at this point.
    try:
        allure.attach(
            page.screenshot(),
            name="Screenshot on Failure",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception as exc:  # noqa: BLE001
        log.warning("Could not attach screenshot to Allure: %s", exc)

    # 2. Capture video path before the context closes.
    video_path: str | None = None
    try:
        if page.video:
            video_path = page.video.path()
    except Exception:  # noqa: BLE001
        pass

    # 3. Close the context explicitly so Playwright flushes the video file.
    #    pytest-playwright's own context fixture will attempt another close
    #    during teardown, which is a safe no-op.
    try:
        context.close()
    except Exception:  # noqa: BLE001
        pass

    # 4. Attach video now that the file has been written.
    if video_path:
        try:
            vp = Path(video_path)
            if vp.exists():
                allure.attach(
                    vp.read_bytes(),
                    name="Video on Failure",
                    attachment_type=allure.attachment_type.WEBM,
                )
        except Exception as exc:  # noqa: BLE001
            log.warning("Could not attach video to Allure: %s", exc)
