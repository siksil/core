"""Coordinator for Syncthru integration."""

import asyncio
from datetime import timedelta
import logging

from pysyncthru import ConnectionMode, SyncThru

from inpui.config_entries import ConfigEntry
from inpui.const import CONF_URL
from inpui.core import HomeAssistant
from inpui.helpers.aiohttp_client import async_get_clientsession
from inpui.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

type SyncThruConfigEntry = ConfigEntry[SyncthruCoordinator]


class SyncthruCoordinator(DataUpdateCoordinator[SyncThru]):
    """Class to manage fetching Syncthru data."""

    def __init__(self, hass: HomeAssistant, entry: SyncThruConfigEntry) -> None:
        """Initialize the Syncthru coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            config_entry=entry,
            update_interval=timedelta(seconds=30),
        )
        self.syncthru = SyncThru(
            entry.data[CONF_URL],
            async_get_clientsession(hass),
            connection_mode=ConnectionMode.API,
        )

    async def _async_update_data(self) -> SyncThru:
        async with asyncio.timeout(10):
            await self.syncthru.update()
        if self.syncthru.is_unknown_state():
            raise UpdateFailed(
                f"Configured printer at {self.syncthru.url} does not respond."
            )
        return self.syncthru
