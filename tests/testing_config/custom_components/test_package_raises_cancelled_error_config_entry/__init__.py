"""Provide a mock package component."""

import asyncio

from inpui.config_entries import ConfigEntry
from inpui.core import HomeAssistant
from inpui.helpers.typing import ConfigType


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Mock a successful setup."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Mock an leaked cancellation, without our own task being cancelled."""
    raise asyncio.CancelledError
