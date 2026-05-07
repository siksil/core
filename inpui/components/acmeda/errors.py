"""Errors for the Acmeda Pulse component."""

from inpui.exceptions import HomeAssistantError


class PulseException(HomeAssistantError):
    """Base class for Acmeda Pulse exceptions."""


class CannotConnect(PulseException):
    """Unable to connect to the bridge."""
