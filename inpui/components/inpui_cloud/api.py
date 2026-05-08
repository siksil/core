import logging
from typing import Dict, Any, List

import aiohttp
from inpui.core import HomeAssistant
from inpui.helpers.aiohttp_client import async_get_clientsession

from .const import ATTR_HARDWARE_PAIR_URL, ATTR_HARDWARE_HEARTBEAT_URL, ATTR_ICE_SERVERS_URL

_LOGGER = logging.getLogger(__name__)

class InpuiCloudAPI:
    """Interface to the Inpui Cloud Central API."""

    def __init__(self, hass: HomeAssistant, jwt_token: str = None):
        self.hass = hass
        self.session = async_get_clientsession(hass)
        self.jwt_token = jwt_token
        self.headers = {
            "Content-Type": "application/json"
        }
        if jwt_token:
            self.headers["Authorization"] = f"Bearer {jwt_token}"

    async def pair_device(self, pairing_code: str, hw_uuid: str, mac: str = None) -> Dict[str, Any]:
        """Claim a pairing code and get hub config."""
        try:
            async with self.session.post(
                ATTR_HARDWARE_PAIR_URL,
                json={
                    "pairing_code": pairing_code,
                    "hw_uuid": hw_uuid,
                    "mac_address": mac,
                    "firmware_version": "aeon-os-1.0",
                    "ha_version": "master"
                },
                timeout=10
            ) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as err:
            _LOGGER.error("Error pairing device: %s", err)
            raise

    async def send_heartbeat(self, hub_id: str):
        """Send a heartbeat to the central API."""
        try:
            async with self.session.post(
                f"{ATTR_HARDWARE_HEARTBEAT_URL}?hub_id={hub_id}",
                headers=self.headers,
                timeout=5
            ) as response:
                response.raise_for_status()
        except aiohttp.ClientError as err:
            _LOGGER.debug("Heartbeat failed: %s", err)

    async def get_ice_servers(self, hub_id: str) -> List[Dict[str, Any]]:
        """Fetch fresh ICE servers."""
        try:
            async with self.session.get(
                f"{ATTR_ICE_SERVERS_URL}?hub_id={hub_id}",
                headers=self.headers,
                timeout=10
            ) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching ICE servers: %s", err)
            return []
