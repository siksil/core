"""Coordinator for the Dexcom integration."""

from datetime import timedelta
import logging

from pydexcom import Dexcom, GlucoseReading

from inpui.config_entries import ConfigEntry
from inpui.core import HomeAssistant
from inpui.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

_SCAN_INTERVAL = timedelta(seconds=180)

type DexcomConfigEntry = ConfigEntry[DexcomCoordinator]


class DexcomCoordinator(DataUpdateCoordinator[GlucoseReading | None]):
    """Dexcom Coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: DexcomConfigEntry,
        dexcom: Dexcom,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=_SCAN_INTERVAL,
        )
        self.dexcom = dexcom

    async def _async_update_data(self) -> GlucoseReading | None:
        """Fetch data from API endpoint."""
        return await self.hass.async_add_executor_job(
            self.dexcom.get_current_glucose_reading
        )
