"""The OurGroceries integration."""

from __future__ import annotations

from aiohttp import ClientError
from ourgroceries import OurGroceries
from ourgroceries.exceptions import InvalidLoginException

from inpui.config_entries import ConfigEntry
from inpui.const import CONF_PASSWORD, CONF_USERNAME, Platform
from inpui.core import HomeAssistant
from inpui.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .coordinator import OurGroceriesDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.TODO]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up OurGroceries from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    data = entry.data
    og = OurGroceries(data[CONF_USERNAME], data[CONF_PASSWORD])
    try:
        await og.login()
    except (TimeoutError, ClientError) as error:
        raise ConfigEntryNotReady from error
    except InvalidLoginException:
        return False

    coordinator = OurGroceriesDataUpdateCoordinator(hass, entry, og)
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
