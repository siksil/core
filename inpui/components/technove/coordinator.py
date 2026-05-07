"""DataUpdateCoordinator for TechnoVE."""

from __future__ import annotations

from technove import Station as TechnoVEStation, TechnoVE, TechnoVEError

from inpui.config_entries import ConfigEntry
from inpui.const import CONF_HOST
from inpui.core import HomeAssistant
from inpui.helpers.aiohttp_client import async_get_clientsession
from inpui.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER, SCAN_INTERVAL

type TechnoVEConfigEntry = ConfigEntry[TechnoVEDataUpdateCoordinator]


class TechnoVEDataUpdateCoordinator(DataUpdateCoordinator[TechnoVEStation]):
    """Class to manage fetching TechnoVE data from single endpoint."""

    config_entry: TechnoVEConfigEntry

    def __init__(self, hass: HomeAssistant, config_entry: TechnoVEConfigEntry) -> None:
        """Initialize global TechnoVE data updater."""
        self.technove = TechnoVE(
            config_entry.data[CONF_HOST],
            session=async_get_clientsession(hass),
        )
        super().__init__(
            hass,
            LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> TechnoVEStation:
        """Fetch data from TechnoVE."""
        try:
            station = await self.technove.update()
        except TechnoVEError as error:
            raise UpdateFailed(f"Invalid response from API: {error}") from error

        return station
