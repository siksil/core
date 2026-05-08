"""The errors of Epson integration."""

from inpui import exceptions


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class PoweredOff(exceptions.HomeAssistantError):
    """Error to indicate projector is off."""
