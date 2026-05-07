"""Diagnostics support for Workday."""

from __future__ import annotations

from typing import Any

from inpui.config_entries import ConfigEntry
from inpui.core import HomeAssistant


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return {
        "config_entry": entry,
    }
