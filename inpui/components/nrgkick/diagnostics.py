"""Diagnostics support for NRGkick."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from inpui.components.diagnostics import async_redact_data
from inpui.const import (
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    CONF_PASSWORD,
    CONF_USERNAME,
)
from inpui.core import HomeAssistant

from .coordinator import NRGkickConfigEntry

TO_REDACT = {
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    "altitude",
    CONF_PASSWORD,
    CONF_USERNAME,
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: NRGkickConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(
        {
            "entry_data": entry.data,
            "coordinator_data": asdict(entry.runtime_data.data),
        },
        TO_REDACT,
    )
