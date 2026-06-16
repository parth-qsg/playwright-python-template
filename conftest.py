"""Root conftest — registers all framework fixture modules and shared hooks."""

import pytest

# Register fixture modules as plugins so their @pytest.fixture functions
# are available to every test without per-file imports.
pytest_plugins = [
    "framework.fixtures.shared",
    "framework.fixtures.ui_fixtures",
]


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--config",
        action="store",
        default=None,
        metavar="PATH",
        help="Path to JSON config file (default: config.json)",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Set up colorlog console handler before any test output is emitted."""
    import logging

    try:
        import colorlog

        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(
                "%(log_color)s%(levelname)-8s%(reset)s %(name)s — %(message)s"
            )
        )
        root = logging.getLogger()
        root.handlers.clear()
        root.addHandler(handler)
        root.setLevel(logging.WARNING)
        logging.getLogger("framework").setLevel(logging.INFO)
    except ImportError:
        pass  # colorlog optional; standard logging still works


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call):
    """Make the test outcome available inside fixtures via ``request.node.rep_call``."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
