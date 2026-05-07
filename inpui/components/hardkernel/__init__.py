"""The Hardkernel integration."""

from __future__ import annotations

from inpui.components.hassio import get_os_info
from inpui.config_entries import ConfigEntry
from inpui.core import HomeAssistant
from inpui.exceptions import ConfigEntryNotReady
from inpui.helpers.hassio import is_hassio


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a Hardkernel config entry."""
    if not is_hassio(hass):
        # Not running under supervisor, Home Assistant may have been migrated
        hass.async_create_task(hass.config_entries.async_remove(entry.entry_id))
        return False

    if (os_info := get_os_info(hass)) is None:
        # The hassio integration has not yet fetched data from the supervisor
        raise ConfigEntryNotReady

    board: str | None
    if (board := os_info.get("board")) is None or not board.startswith("odroid"):
        # Not running on a Hardkernel board, Home Assistant may have been migrated
        hass.async_create_task(hass.config_entries.async_remove(entry.entry_id))
        return False

    return True
