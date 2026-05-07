"""Errors for the Mikrotik component."""

from inpui.exceptions import HomeAssistantError


class CannotConnect(HomeAssistantError):
    """Unable to connect to the hub."""


class LoginError(HomeAssistantError):
    """Component got logged out."""
