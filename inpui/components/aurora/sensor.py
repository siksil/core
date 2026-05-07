"""Support for Aurora Forecast sensor."""

from __future__ import annotations

from inpui.components.sensor import SensorEntity, SensorStateClass
from inpui.const import PERCENTAGE
from inpui.core import HomeAssistant
from inpui.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import AuroraConfigEntry
from .entity import AuroraEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AuroraConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the sensor platform."""

    async_add_entities(
        [
            AuroraSensor(
                coordinator=entry.runtime_data,
                translation_key="visibility",
            )
        ]
    )


class AuroraSensor(AuroraEntity, SensorEntity):
    """Implementation of an aurora sensor."""

    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> int:
        """Return % chance the aurora is visible."""
        return self.coordinator.data
