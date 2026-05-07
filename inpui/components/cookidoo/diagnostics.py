"""Diagnostics for the Cookidoo integration."""

from dataclasses import asdict
from typing import Any

from inpui.components.diagnostics import async_redact_data
from inpui.const import CONF_PASSWORD
from inpui.core import HomeAssistant

from .coordinator import CookidooConfigEntry

TO_REDACT = [
    CONF_PASSWORD,
]


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: CookidooConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return {
        "entry_data": async_redact_data(entry.data, TO_REDACT),
        "data": asdict(entry.runtime_data.data),
        "user": asdict(entry.runtime_data.user),
    }
