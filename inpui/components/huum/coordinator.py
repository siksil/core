"""DataUpdateCoordinator for Huum."""

from __future__ import annotations

from datetime import timedelta
import logging

from huum.exceptions import Forbidden, NotAuthenticated
from huum.huum import Huum
from huum.schemas import HuumStatusResponse

from inpui.config_entries import ConfigEntry
from inpui.const import CONF_PASSWORD, CONF_USERNAME
from inpui.core import HomeAssistant
from inpui.exceptions import ConfigEntryAuthFailed
from inpui.helpers.aiohttp_client import async_get_clientsession
from inpui.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

type HuumConfigEntry = ConfigEntry[HuumDataUpdateCoordinator]

_LOGGER = logging.getLogger(__name__)
UPDATE_INTERVAL = timedelta(seconds=30)


class HuumDataUpdateCoordinator(DataUpdateCoordinator[HuumStatusResponse]):
    """Class to manage fetching data from the API."""

    config_entry: HuumConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: HuumConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
            config_entry=config_entry,
        )

        self.huum = Huum(
            config_entry.data[CONF_USERNAME],
            config_entry.data[CONF_PASSWORD],
            session=async_get_clientsession(hass),
        )

    async def _async_update_data(self) -> HuumStatusResponse:
        """Get the latest status data."""

        try:
            return await self.huum.status()
        except (Forbidden, NotAuthenticated) as err:
            raise ConfigEntryAuthFailed(
                "Could not log in to Huum with given credentials"
            ) from err
