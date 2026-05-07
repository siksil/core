"""Diagnostics support for TRMNL."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from inpui.components.diagnostics import async_redact_data
from inpui.core import HomeAssistant

from .coordinator import TRMNLConfigEntry

TO_REDACT = {"mac_address"}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: TRMNLConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "data": [
            async_redact_data(asdict(device), TO_REDACT)
            for device in entry.runtime_data.data.values()
        ],
    }
