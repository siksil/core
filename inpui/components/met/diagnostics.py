"""Diagnostics support for Met.no integration."""

from typing import Any

from inpui.components.diagnostics import async_redact_data
from inpui.const import CONF_LATITUDE, CONF_LONGITUDE
from inpui.core import HomeAssistant

from .coordinator import MetWeatherConfigEntry

TO_REDACT = [
    CONF_LATITUDE,
    CONF_LONGITUDE,
]


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: MetWeatherConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator_data = entry.runtime_data.data

    return {
        "entry_data": async_redact_data(entry.data, TO_REDACT),
        "data": {
            "current_weather_data": coordinator_data.current_weather_data,
            "daily_forecast": coordinator_data.daily_forecast,
            "hourly_forecast": coordinator_data.hourly_forecast,
        },
    }
