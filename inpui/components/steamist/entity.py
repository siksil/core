"""Support for Steamist sensors."""

from __future__ import annotations

from aiosteamist import SteamistStatus

from inpui.config_entries import ConfigEntry
from inpui.const import CONF_HOST, CONF_MODEL
from inpui.helpers import device_registry as dr
from inpui.helpers.device_registry import DeviceInfo
from inpui.helpers.entity import Entity, EntityDescription
from inpui.helpers.update_coordinator import CoordinatorEntity

from .coordinator import SteamistDataUpdateCoordinator


class SteamistEntity(CoordinatorEntity[SteamistDataUpdateCoordinator], Entity):
    """Representation of a Steamist entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SteamistDataUpdateCoordinator,
        entry: ConfigEntry,
        description: EntityDescription,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        if entry.unique_id:  # Only present if UDP broadcast works
            self._attr_device_info = DeviceInfo(
                connections={(dr.CONNECTION_NETWORK_MAC, entry.unique_id)},
                manufacturer="Steamist",
                model=entry.data[CONF_MODEL],
                configuration_url=f"http://{entry.data[CONF_HOST]}",
            )

    @property
    def _status(self) -> SteamistStatus:
        """Return the steamist status."""
        return self.coordinator.data
