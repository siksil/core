"""Set up Inpui Cloud from a config entry."""

import logging
from datetime import timedelta

from inpui.config_entries import ConfigEntry
from inpui.core import HomeAssistant
from inpui.helpers.event import async_track_time_interval

from .const import DOMAIN, CONF_JWT_TOKEN, CONF_TUNNEL_TOKEN, CONF_HUB_ID
from .api import InpuiCloudAPI
from .tunnel import CloudflareTunnel

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Inpui Cloud from a config entry."""
    data = entry.data

    api = InpuiCloudAPI(hass=hass, jwt_token=data[CONF_JWT_TOKEN])
    tunnel = CloudflareTunnel(token=data[CONF_TUNNEL_TOKEN])

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "api": api,
        "tunnel": tunnel,
        "hub_id": data[CONF_HUB_ID],
    }

    # Start the tunnel as a managed background task tied to this entry's lifecycle.
    # Using entry.async_create_background_task instead of raw asyncio.create_task
    # ensures the task is automatically cancelled when the entry is unloaded.
    entry.async_create_background_task(
        hass,
        tunnel.start_managed(),
        name=f"inpui_cloud_tunnel_{entry.entry_id}",
    )

    # Set up periodic heartbeat
    async def send_heartbeat(_now):
        try:
            await api.send_heartbeat(data[CONF_HUB_ID])
        except Exception:
            _LOGGER.debug("Heartbeat failed", exc_info=True)

    entry.async_on_unload(
        async_track_time_interval(hass, send_heartbeat, timedelta(seconds=60))
    )

    # Trigger first heartbeat
    await send_heartbeat(None)

    await hass.config_entries.async_forward_entry_setups(entry, ["binary_sensor"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["binary_sensor"])
    if unload_ok:
        entry_data = hass.data[DOMAIN].pop(entry.entry_id, None)
        if entry_data:
            await entry_data["tunnel"].stop()

    return unload_ok
