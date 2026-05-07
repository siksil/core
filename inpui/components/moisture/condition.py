"""Provides conditions for moisture."""

from __future__ import annotations

from inpui.components.binary_sensor import (
    DOMAIN as BINARY_SENSOR_DOMAIN,
    BinarySensorDeviceClass,
)
from inpui.components.sensor import DOMAIN as SENSOR_DOMAIN, SensorDeviceClass
from inpui.const import PERCENTAGE, STATE_OFF, STATE_ON
from inpui.core import HomeAssistant
from inpui.helpers.automation import DomainSpec
from inpui.helpers.condition import (
    Condition,
    make_entity_numerical_condition,
    make_entity_state_condition,
)

_MOISTURE_BINARY_DOMAIN_SPECS = {
    BINARY_SENSOR_DOMAIN: DomainSpec(
        device_class=BinarySensorDeviceClass.MOISTURE,
    )
}

_MOISTURE_NUMERICAL_DOMAIN_SPECS = {
    SENSOR_DOMAIN: DomainSpec(device_class=SensorDeviceClass.MOISTURE),
}

CONDITIONS: dict[str, type[Condition]] = {
    "is_detected": make_entity_state_condition(_MOISTURE_BINARY_DOMAIN_SPECS, STATE_ON),
    "is_not_detected": make_entity_state_condition(
        _MOISTURE_BINARY_DOMAIN_SPECS, STATE_OFF
    ),
    "is_value": make_entity_numerical_condition(
        _MOISTURE_NUMERICAL_DOMAIN_SPECS, PERCENTAGE
    ),
}


async def async_get_conditions(hass: HomeAssistant) -> dict[str, type[Condition]]:
    """Return the conditions for moisture."""
    return CONDITIONS
