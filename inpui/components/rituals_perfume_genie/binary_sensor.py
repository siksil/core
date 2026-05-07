"""Support for Rituals Perfume Genie binary sensors."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from pyrituals import Diffuser

from inpui.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from inpui.config_entries import ConfigEntry
from inpui.const import EntityCategory
from inpui.core import HomeAssistant
from inpui.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import RitualsDataUpdateCoordinator
from .entity import DiffuserEntity


@dataclass(frozen=True, kw_only=True)
class RitualsBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Class describing Rituals binary sensor entities."""

    is_on_fn: Callable[[Diffuser], bool]
    has_fn: Callable[[Diffuser], bool]


ENTITY_DESCRIPTIONS = (
    RitualsBinarySensorEntityDescription(
        key="charging",
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
        entity_category=EntityCategory.DIAGNOSTIC,
        is_on_fn=lambda diffuser: diffuser.charging,
        has_fn=lambda diffuser: diffuser.has_battery,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the diffuser binary sensors."""
    coordinators: dict[str, RitualsDataUpdateCoordinator] = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    async_add_entities(
        RitualsBinarySensorEntity(coordinator, description)
        for coordinator in coordinators.values()
        for description in ENTITY_DESCRIPTIONS
        if description.has_fn(coordinator.diffuser)
    )


class RitualsBinarySensorEntity(DiffuserEntity, BinarySensorEntity):
    """Defines a Rituals binary sensor entity."""

    entity_description: RitualsBinarySensorEntityDescription

    @property
    def is_on(self) -> bool:
        """Return the state of the binary sensor."""
        return self.entity_description.is_on_fn(self.coordinator.diffuser)
