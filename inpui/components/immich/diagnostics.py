"""Diagnostics support for immich."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from inpui.components.diagnostics import async_redact_data
from inpui.const import CONF_API_KEY, CONF_HOST
from inpui.core import HomeAssistant

from .coordinator import ImmichConfigEntry

TO_REDACT = {CONF_API_KEY, CONF_HOST}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ImmichConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data

    return {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "data": asdict(coordinator.data),
    }
