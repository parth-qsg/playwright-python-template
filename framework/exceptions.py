"""Framework-wide exception hierarchy."""


class FrameworkError(Exception):
    """Base exception for all framework errors."""


class ConfigurationError(FrameworkError):
    """Raised when configuration is missing or invalid."""


class AuthenticationError(FrameworkError):
    """Raised when login / token refresh fails."""


class APIError(FrameworkError):
    """Raised for unexpected API response codes."""

    def __init__(self, message: str, status_code: int = 0, response_text: str = ""):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class APIConnectionError(APIError):
    """Raised when a network connection to the API fails."""


class TokenRefreshError(AuthenticationError):
    """Raised when token refresh fails."""


class UIError(FrameworkError):
    """Raised for unexpected UI state or interaction failures."""


class PageLoadError(UIError):
    """Raised when a page does not reach the expected state."""


class ElementNotFoundError(UIError):
    """Raised when an expected element is not present."""


class AssertionCollectionError(FrameworkError):
    """Raised by SoftAssertions.assert_all() when one or more checks failed."""


class CleanupError(FrameworkError):
    """Raised when test resource cleanup fails."""


class TestDataError(FrameworkError):
    """Raised when test data is missing or malformed."""


class WaitTimeoutError(FrameworkError):
    """Raised when poll_until() or wait_for_condition() times out."""
