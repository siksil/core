"""Provides conditions for occupancy."""

from inpui.components.binary_sensor import (
    DOMAIN as BINARY_SENSOR_DOMAIN,
    BinarySensorDeviceClass,
)
from inpui.const import STATE_OFF, STATE_ON
from inpui.core import HomeAssistant
from inpui.helpers.automation import DomainSpec
from inpui.helpers.condition import Condition, make_entity_state_condition

_OCCUPANCY_DOMAIN_SPECS = {
    BINARY_SENSOR_DOMAIN: DomainSpec(device_class=BinarySensorDeviceClass.OCCUPANCY)
}


CONDITIONS: dict[str, type[Condition]] = {
    "is_detected": make_entity_state_condition(_OCCUPANCY_DOMAIN_SPECS, STATE_ON),
    "is_not_detected": make_entity_state_condition(_OCCUPANCY_DOMAIN_SPECS, STATE_OFF),
}


async def async_get_conditions(hass: HomeAssistant) -> dict[str, type[Condition]]:
    """Return the conditions for occupancy."""
    return CONDITIONS
