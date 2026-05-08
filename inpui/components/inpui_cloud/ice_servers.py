import logging
from typing import List, Dict, Any
from inpui.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

async def async_get_ice_servers(hass: HomeAssistant, hub_id: str, api: Any) -> List[Dict[str, Any]]:
    """
    Fetch ICE servers from Inpui Cloud.
    This can be hooked into HA's camera WebRTC system.
    """
    try:
        ice_servers = await api.get_ice_servers(hub_id)
        return ice_servers
    except Exception as err:
        _LOGGER.error("Failed to fetch ICE servers: %s", err)
        return []
