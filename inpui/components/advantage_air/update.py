"""Advantage Air Update platform."""

from inpui.components.update import UpdateEntity
from inpui.core import HomeAssistant
from inpui.helpers.device_registry import DeviceInfo
from inpui.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import AdvantageAirDataConfigEntry
from .const import DOMAIN
from .coordinator import AdvantageAirCoordinator
from .entity import AdvantageAirEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: AdvantageAirDataConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up AdvantageAir update platform."""

    coordinator = config_entry.runtime_data

    async_add_entities([AdvantageAirApp(coordinator)])


class AdvantageAirApp(AdvantageAirEntity, UpdateEntity):
    """Representation of Advantage Air App."""

    _attr_name = "App"

    def __init__(self, coordinator: AdvantageAirCoordinator) -> None:
        """Initialize the Advantage Air App."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.data["system"]["rid"])},
            manufacturer="Advantage Air",
            model=self.coordinator.data["system"]["sysType"],
            name=self.coordinator.data["system"]["name"],
            sw_version=self.coordinator.data["system"]["myAppRev"],
        )

    @property
    def installed_version(self) -> str:
        """Return the current app version."""
        return self.coordinator.data["system"]["myAppRev"]

    @property
    def latest_version(self) -> str:
        """Return if there is an update."""
        if self.coordinator.data["system"]["needsUpdate"]:
            return "Needs Update"
        return self.installed_version
