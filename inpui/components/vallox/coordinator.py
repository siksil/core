"""Coordinator for Vallox ventilation units."""

from __future__ import annotations

import logging

from vallox_websocket_api import MetricData, Vallox, ValloxApiException

from inpui.config_entries import ConfigEntry
from inpui.const import CONF_NAME
from inpui.core import HomeAssistant
from inpui.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import STATE_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class ValloxDataUpdateCoordinator(DataUpdateCoordinator[MetricData]):
    """The DataUpdateCoordinator for Vallox."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        client: Vallox,
    ) -> None:
        """Initialize Vallox data coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=f"{config_entry.data[CONF_NAME]} DataUpdateCoordinator",
            update_interval=STATE_SCAN_INTERVAL,
        )
        self.client = client

    async def _async_update_data(self) -> MetricData:
        """Fetch state update."""
        _LOGGER.debug("Updating Vallox state cache")

        try:
            return await self.client.fetch_metric_data()
        except ValloxApiException as err:
            raise UpdateFailed("Error during state cache update") from err
