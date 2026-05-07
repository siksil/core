"""Refoss helpers functions."""

from __future__ import annotations

from refoss_ha.discovery import Discovery

from inpui.core import HomeAssistant
from inpui.helpers import singleton


@singleton.singleton("refoss_discovery_server")
async def refoss_discovery_server(hass: HomeAssistant) -> Discovery:
    """Get refoss Discovery server."""
    discovery_server = Discovery()
    await discovery_server.initialize()
    return discovery_server
