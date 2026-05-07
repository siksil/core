"""Define the Nanoleaf data coordinator."""

from datetime import timedelta
import logging

from aionanoleaf2 import InvalidToken, Nanoleaf, Unavailable

from inpui.config_entries import ConfigEntry
from inpui.core import HomeAssistant
from inpui.exceptions import ConfigEntryAuthFailed
from inpui.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

type NanoleafConfigEntry = ConfigEntry[NanoleafCoordinator]


class NanoleafCoordinator(DataUpdateCoordinator[None]):
    """Class to manage fetching Nanoleaf data."""

    config_entry: NanoleafConfigEntry

    def __init__(
        self, hass: HomeAssistant, config_entry: NanoleafConfigEntry, nanoleaf: Nanoleaf
    ) -> None:
        """Initialize the Nanoleaf data coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name="Nanoleaf",
            update_interval=timedelta(minutes=1),
        )
        self.nanoleaf = nanoleaf

    async def _async_update_data(self) -> None:
        try:
            await self.nanoleaf.get_info()
        except Unavailable as err:
            raise UpdateFailed from err
        except InvalidToken as err:
            raise ConfigEntryAuthFailed from err
