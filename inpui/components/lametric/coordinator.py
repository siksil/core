"""DataUpdateCoordinator for the LaMatric integration."""

from __future__ import annotations

from demetriek import Device, LaMetricAuthenticationError, LaMetricDevice, LaMetricError

from inpui.config_entries import ConfigEntry
from inpui.const import CONF_API_KEY, CONF_HOST
from inpui.core import HomeAssistant
from inpui.exceptions import ConfigEntryAuthFailed
from inpui.helpers.aiohttp_client import async_get_clientsession
from inpui.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER, SCAN_INTERVAL

type LaMetricConfigEntry = ConfigEntry[LaMetricDataUpdateCoordinator]


class LaMetricDataUpdateCoordinator(DataUpdateCoordinator[Device]):
    """The LaMetric Data Update Coordinator."""

    config_entry: LaMetricConfigEntry

    def __init__(self, hass: HomeAssistant, entry: LaMetricConfigEntry) -> None:
        """Initialize the LaMatric coordinator."""
        self.lametric = LaMetricDevice(
            host=entry.data[CONF_HOST],
            api_key=entry.data[CONF_API_KEY],
            session=async_get_clientsession(hass),
        )

        super().__init__(
            hass, LOGGER, config_entry=entry, name=DOMAIN, update_interval=SCAN_INTERVAL
        )

    async def _async_update_data(self) -> Device:
        """Fetch device information of the LaMetric device."""
        try:
            return await self.lametric.device()
        except LaMetricAuthenticationError as err:
            raise ConfigEntryAuthFailed from err
        except LaMetricError as ex:
            raise UpdateFailed(
                "Could not fetch device information from LaMetric device"
            ) from ex
