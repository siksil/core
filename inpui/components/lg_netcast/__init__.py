"""The lg_netcast component."""

from typing import Final

from pylgnetcast import LgNetCastClient

from inpui.config_entries import ConfigEntry
from inpui.const import CONF_ACCESS_TOKEN, CONF_HOST, Platform
from inpui.core import HomeAssistant
from inpui.helpers import config_validation as cv

from .const import DOMAIN

PLATFORMS: Final[list[Platform]] = [Platform.MEDIA_PLAYER]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

type LgNetCastConfigEntry = ConfigEntry[LgNetCastClient]


async def async_setup_entry(
    hass: HomeAssistant, config_entry: LgNetCastConfigEntry
) -> bool:
    """Set up a config entry."""
    host = config_entry.data[CONF_HOST]
    access_token = config_entry.data[CONF_ACCESS_TOKEN]

    client = LgNetCastClient(host, access_token)

    config_entry.runtime_data = client

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: LgNetCastConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
