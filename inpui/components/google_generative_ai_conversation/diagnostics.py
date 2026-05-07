"""Diagnostics support for Google Generative AI Conversation."""

from __future__ import annotations

from typing import Any

from inpui.components.diagnostics import async_redact_data
from inpui.config_entries import ConfigEntry
from inpui.const import CONF_API_KEY
from inpui.core import HomeAssistant

TO_REDACT = {CONF_API_KEY}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(
        {
            "title": entry.title,
            "data": entry.data,
            "options": entry.options,
            "subentries": dict(entry.subentries),
        },
        TO_REDACT,
    )
