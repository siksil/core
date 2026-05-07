"""Diagnostics support for Satel Integra."""

from __future__ import annotations

from typing import Any

from inpui.components.diagnostics import async_redact_data
from inpui.config_entries import ConfigEntry
from inpui.const import CONF_CODE
from inpui.core import HomeAssistant

TO_REDACT = {CONF_CODE}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for the config entry."""
    diag: dict[str, Any] = {}

    diag["config_entry_data"] = dict(entry.data)
    diag["config_entry_options"] = async_redact_data(entry.options, TO_REDACT)

    diag["subentries"] = dict(entry.subentries)

    return diag
