"""Custom exceptions for the devolo_home_control integration."""

from inpui.exceptions import HomeAssistantError


class CredentialsInvalid(HomeAssistantError):
    """Given credentials are invalid."""


class UuidChanged(HomeAssistantError):
    """UUID of the user changed."""
