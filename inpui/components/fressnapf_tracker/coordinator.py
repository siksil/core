"""Data update coordinator for Fressnapf Tracker integration."""

from datetime import timedelta
import logging

from fressnapftracker import (
    ApiClient,
    Device,
    FressnapfTrackerError,
    FressnapfTrackerInvalidDeviceTokenError,
    Tracker,
)

from inpui.config_entries import ConfigEntry
from inpui.core import HomeAssistant
from inpui.exceptions import ConfigEntryAuthFailed
from inpui.helpers.httpx_client import get_async_client
from inpui.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

type FressnapfTrackerConfigEntry = ConfigEntry[
    list[FressnapfTrackerDataUpdateCoordinator]
]


class FressnapfTrackerDataUpdateCoordinator(DataUpdateCoordinator[Tracker]):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: FressnapfTrackerConfigEntry,
        device: Device,
        initial_data: Tracker,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=15),
            config_entry=config_entry,
        )
        self.device = device
        self.client = ApiClient(
            serial_number=device.serialnumber,
            device_token=device.token,
            client=get_async_client(hass),
        )
        self.data = initial_data

    async def _async_update_data(self) -> Tracker:
        try:
            return await self.client.get_tracker()
        except FressnapfTrackerInvalidDeviceTokenError as exception:
            raise ConfigEntryAuthFailed(
                translation_domain=DOMAIN,
                translation_key="invalid_auth",
            ) from exception
        except FressnapfTrackerError as exception:
            raise UpdateFailed(exception) from exception
