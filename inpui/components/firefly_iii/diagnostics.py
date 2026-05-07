"""Diagnostics for the Firefly III integration."""

from __future__ import annotations

from typing import Any

from inpui.components.diagnostics import async_redact_data
from inpui.const import CONF_API_KEY, CONF_URL
from inpui.core import HomeAssistant

from . import FireflyConfigEntry
from .coordinator import FireflyDataUpdateCoordinator

TO_REDACT = [CONF_API_KEY, CONF_URL]


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: FireflyConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: FireflyDataUpdateCoordinator = entry.runtime_data

    return {
        "config_entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "data": {"primary_currency": coordinator.data.primary_currency.to_dict()},
    }
