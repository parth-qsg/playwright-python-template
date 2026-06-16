"""PageFactory — string-keyed registry of all BasePage subclasses."""

from __future__ import annotations

import logging
from typing import ClassVar, TYPE_CHECKING

from framework.ui.base_page import BasePage

if TYPE_CHECKING:
    from playwright.sync_api import Page

log = logging.getLogger(__name__)


class PageFactory:
    """
    Registry of page types.  Tests use human-readable string keys::

        login = ui_context.page_factory("Login Page")

    Pages register themselves when their module is first imported::

        PageFactory.register("Login Page", LoginPage)
    """

    _registry: ClassVar[dict[str, type[BasePage]]] = {}

    @classmethod
    def register(cls, name: str, page_class: type[BasePage]) -> None:
        cls._registry[name] = page_class
        log.debug("PageFactory registered: '%s' → %s", name, page_class.__name__)

    @classmethod
    def create(cls, page_type: str, page: "Page", base_url: str) -> BasePage:
        if page_type not in cls._registry:
            available = sorted(cls._registry)
            raise ValueError(
                f"Unknown page type: '{page_type}'. "
                f"Available: {available}"
            )
        return cls._registry[page_type](page, base_url)

    @classmethod
    def registered_types(cls) -> list[str]:
        return sorted(cls._registry)
