"""Support for monitoring the state of UpCloud servers."""

from inpui.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from inpui.core import HomeAssistant
from inpui.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import UpCloudConfigEntry
from .entity import UpCloudServerEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: UpCloudConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the UpCloud server binary sensor."""
    coordinator = config_entry.runtime_data
    entities = [UpCloudBinarySensor(config_entry, uuid) for uuid in coordinator.data]
    async_add_entities(entities, True)


class UpCloudBinarySensor(UpCloudServerEntity, BinarySensorEntity):
    """Representation of an UpCloud server sensor."""

    _attr_device_class = BinarySensorDeviceClass.POWER
