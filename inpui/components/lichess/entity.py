"""Base entity for Lichess integration."""

from typing import TYPE_CHECKING

from inpui.helpers.device_registry import DeviceEntryType, DeviceInfo
from inpui.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import LichessCoordinator


class LichessEntity(CoordinatorEntity[LichessCoordinator]):
    """Base entity for Lichess integration."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: LichessCoordinator) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        if TYPE_CHECKING:
            assert coordinator.config_entry.unique_id is not None
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.unique_id)},
            entry_type=DeviceEntryType.SERVICE,
            manufacturer="Lichess",
        )
