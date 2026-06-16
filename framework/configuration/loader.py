"""ConfigLoader — reads JSON config file and applies environment-variable overrides."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from framework.configuration.config import Configuration

log = logging.getLogger(__name__)

_DEFAULT_BASE_URL = ""


class ConfigLoader:
    """Reads a JSON config file and overlays environment-variable overrides."""

    @classmethod
    def initialize(cls, config_path: str | None = None) -> None:
        """
        Initialize the Configuration singleton from *config_path* (JSON).

        Precedence (highest wins):  env var  >  JSON file  >  built-in default
        """
        load_dotenv(override=False)  # .env does NOT override already-set env vars

        path = Path(config_path) if config_path else Path("config.json")
        raw: dict = {}
        if path.exists():
            with path.open() as f:
                raw = json.load(f)
            log.info("Config loaded from: %s", path)
        else:
            log.warning("Config file not found: %s — using defaults + env vars", path)

        aut = raw.get("AUT", {})
        tests = raw.get("tests", {})

        # AUT — env vars take precedence over JSON
        Configuration.base_url = os.getenv(
            "BASE_URL", aut.get("base_url", _DEFAULT_BASE_URL)
        )
        Configuration.ui_viewport = aut.get("ui_viewport", {})

        # Credentials — JSON base, then env-var overrides
        creds: dict = aut.get("credentials", {})
        for role, env_prefix in (("admin", "APP_ADMIN"), ("member", "APP_MEMBER")):
            role_creds = creds.get(role, {})
            role_creds["username"] = os.getenv(
                f"{env_prefix}_USERNAME",
                os.getenv("TEST_USERNAME", role_creds.get("username", "")),
            )
            role_creds["password"] = os.getenv(
                f"{env_prefix}_PASSWORD",
                os.getenv("TEST_PASSWORD", role_creds.get("password", "")),
            )
            creds[role] = role_creds
        Configuration.credentials = creds

        # Tests
        Configuration.screenshot_location = tests.get(
            "screenshot_location", "results/screenshots"
        )
        Configuration.headless_mode = tests.get("headless_mode", True)
        Configuration.notes = tests.get("notes", "")

        Configuration._initialized = True
        log.info("Configuration initialized — base_url=%s", Configuration.base_url)
