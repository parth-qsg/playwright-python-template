"""Configuration singleton — class-level attributes, no instantiation."""

from __future__ import annotations

from typing import ClassVar


class Configuration:
    """
    Singleton configuration object using class-level attributes.

    Call ``ConfigLoader.initialize(config_path)`` before accessing values.
    All attributes are class-level so they are shared and accessible as
    ``Configuration.base_url`` without constructing an instance.
    """

    # AUT
    base_url: ClassVar[str] = ""
    credentials: ClassVar[dict] = {}
    ui_viewport: ClassVar[dict] = {}

    # Tests
    screenshot_location: ClassVar[str] = "results/screenshots"
    headless_mode: ClassVar[bool] = True
    notes: ClassVar[str] = ""

    _initialized: ClassVar[bool] = False

    def __new__(cls):
        raise TypeError("Configuration is a singleton; use class attributes directly.")

    @classmethod
    def is_initialized(cls) -> bool:
        return cls._initialized

    @classmethod
    def reset(cls) -> None:
        """Reset to defaults (useful in unit tests of the framework itself)."""
        cls.base_url = ""
        cls.credentials = {}
        cls.ui_viewport = {}
        cls.screenshot_location = "results/screenshots"
        cls.headless_mode = True
        cls.notes = ""
        cls._initialized = False
