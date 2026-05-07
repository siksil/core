"""Support for Smart Meter Texas sensors."""

from typing import Any

from smart_meter_texas import Meter

from inpui.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from inpui.config_entries import ConfigEntry
from inpui.const import CONF_ADDRESS, UnitOfEnergy
from inpui.core import HomeAssistant, callback
from inpui.helpers.entity_platform import AddConfigEntryEntitiesCallback
from inpui.helpers.restore_state import RestoreEntity
from inpui.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DATA_COORDINATOR,
    DATA_SMART_METER,
    DOMAIN,
    ELECTRIC_METER,
    ESIID,
    METER_NUMBER,
)
from .coordinator import SmartMeterTexasCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Smart Meter Texas sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]
    meters = hass.data[DOMAIN][config_entry.entry_id][DATA_SMART_METER].meters

    async_add_entities(
        [SmartMeterTexasSensor(meter, coordinator) for meter in meters], False
    )


# pylint: disable-next=inps-invalid-inheritance # needs fixing
class SmartMeterTexasSensor(
    CoordinatorEntity[SmartMeterTexasCoordinator], RestoreEntity, SensorEntity
):
    """Representation of an Smart Meter Texas sensor."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_available = False

    def __init__(self, meter: Meter, coordinator: SmartMeterTexasCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.meter = meter
        self._attr_name = f"{ELECTRIC_METER} {meter.meter}"
        self._attr_unique_id = f"{meter.esiid}_{meter.meter}"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the device specific state attributes."""
        return {
            METER_NUMBER: self.meter.meter,
            ESIID: self.meter.esiid,
            CONF_ADDRESS: self.meter.address,
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Call when the coordinator has an update."""
        self._attr_available = self.coordinator.last_update_success
        if self._attr_available:
            self._attr_native_value = self.meter.reading
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Subscribe to updates."""
        await super().async_added_to_hass()

        # If the background update finished before
        # we added the entity, there is no need to restore
        # state.
        if self.coordinator.last_update_success:
            return

        if last_state := await self.async_get_last_state():
            self._attr_native_value = last_state.state
            self._attr_available = True
