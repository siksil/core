"""The sia integration."""

from inpui.config_entries import ConfigEntry
from inpui.const import CONF_PORT
from inpui.core import HomeAssistant
from inpui.exceptions import ConfigEntryNotReady

from .const import DOMAIN, PLATFORMS
from .hub import SIAHub


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up sia from a config entry."""
    hub: SIAHub = SIAHub(hass, entry)
    hub.async_setup_hub()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = hub
    try:
        if hub.sia_client:
            await hub.sia_client.async_start(reuse_port=True)
    except OSError as exc:
        raise ConfigEntryNotReady(
            f"SIA Server at port {entry.data[CONF_PORT]} could not start."
        ) from exc
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hub: SIAHub = hass.data[DOMAIN].pop(entry.entry_id)
        await hub.async_shutdown()
    return unload_ok
