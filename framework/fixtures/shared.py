"""Session-scoped shared fixtures: config, base_url, credentials, data_region."""

from __future__ import annotations

import pytest

from framework.configuration.config import Configuration
from framework.configuration.loader import ConfigLoader


@pytest.fixture(scope="session")
def config(request) -> type[Configuration]:
    """Initialize and return the Configuration singleton class."""
    config_path = request.config.getoption("--config", default=None)
    ConfigLoader.initialize(config_path)
    return Configuration


@pytest.fixture(scope="session")
def base_url(config) -> str:
    return config.base_url


@pytest.fixture(scope="session")
def credentials(config) -> dict:
    return config.credentials


@pytest.fixture(scope="session")
def data_region(config) -> dict:
    return getattr(config, "data_region", {})
