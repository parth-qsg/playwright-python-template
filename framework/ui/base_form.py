"""BaseFormComponent — dialog heading, submit, cancel, and alert helpers."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from framework.ui.base_component import BaseComponent

if TYPE_CHECKING:
    from playwright.sync_api import Page

log = logging.getLogger(__name__)


class BaseFormComponent(BaseComponent):
    """
    Extends ``BaseComponent`` with helpers for modal forms/dialogs:
    heading, submit, cancel, and alert-message interactions.
    """

    def __init__(self, page: "Page") -> None:
        super().__init__(page)
        self.dialog_heading = page.locator(
            '[role="dialog"] h2, [role="dialog"] h1'
        ).first
        self.submit_button = page.locator(
            'button[type="submit"], [data-testid="submit-btn"]'
        ).first
        self.cancel_button = page.locator(
            'button:has-text("Cancel"), [data-testid="cancel-btn"]'
        ).first
        self.alert_message = page.locator(
            '[role="alert"], .MuiAlert-message'
        ).first

        self.element_name_mapping.update(
            {
                "Dialog Heading": self.dialog_heading,
                "Submit Button": self.submit_button,
                "Cancel Button": self.cancel_button,
                "Alert Message": self.alert_message,
            }
        )

    def get_heading(self) -> str:
        return self.dialog_heading.inner_text()

    def submit(self) -> None:
        self.click("Submit Button")

    def cancel(self) -> None:
        self.click("Cancel Button")

    def get_alert_text(self) -> str:
        self.wait_for_visible("Alert Message")
        return self.alert_message.inner_text()

    def has_error(self) -> bool:
        return self.alert_message.is_visible()
