"""Snapcast Integration."""

from inpui.config_entries import ConfigEntry
from inpui.const import CONF_HOST, CONF_PORT
from inpui.core import HomeAssistant
from inpui.exceptions import ConfigEntryNotReady
from inpui.helpers import config_validation as cv
from inpui.helpers.typing import ConfigType

from .const import DOMAIN, PLATFORMS
from .coordinator import SnapcastUpdateCoordinator
from .services import async_setup_services

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the component."""
    async_setup_services(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Snapcast from a config entry."""
    coordinator = SnapcastUpdateCoordinator(hass, entry)

    try:
        await coordinator.async_config_entry_first_refresh()
    except OSError as ex:
        raise ConfigEntryNotReady(
            "Could not connect to Snapcast server at "
            f"{entry.data[CONF_HOST]}:{entry.data[CONF_PORT]}"
        ) from ex

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        snapcast_data = hass.data[DOMAIN].pop(entry.entry_id)
        # disconnect from server
        await snapcast_data.disconnect()
    return unload_ok
