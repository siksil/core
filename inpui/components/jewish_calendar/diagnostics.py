"""Diagnostics support for Jewish Calendar integration."""

from dataclasses import asdict
from typing import Any

from inpui.components.diagnostics import async_redact_data
from inpui.const import CONF_LATITUDE, CONF_LONGITUDE
from inpui.core import HomeAssistant

from .const import CONF_ALTITUDE
from .entity import JewishCalendarConfigEntry

TO_REDACT = [
    CONF_ALTITUDE,
    CONF_LATITUDE,
    CONF_LONGITUDE,
]


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: JewishCalendarConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return {
        "entry_data": async_redact_data(entry.data, TO_REDACT),
        "data": async_redact_data(asdict(entry.runtime_data.data), TO_REDACT),
    }
