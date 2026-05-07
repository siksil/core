"""Provides conditions for batteries."""

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

BATTERY_DOMAIN_SPECS = {
    BINARY_SENSOR_DOMAIN: DomainSpec(device_class=BinarySensorDeviceClass.BATTERY)
}
BATTERY_CHARGING_DOMAIN_SPECS = {
    BINARY_SENSOR_DOMAIN: DomainSpec(
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING
    )
}
BATTERY_PERCENTAGE_DOMAIN_SPECS = {
    SENSOR_DOMAIN: DomainSpec(device_class=SensorDeviceClass.BATTERY),
}

CONDITIONS: dict[str, type[Condition]] = {
    "is_low": make_entity_state_condition(BATTERY_DOMAIN_SPECS, STATE_ON),
    "is_not_low": make_entity_state_condition(BATTERY_DOMAIN_SPECS, STATE_OFF),
    "is_charging": make_entity_state_condition(BATTERY_CHARGING_DOMAIN_SPECS, STATE_ON),
    "is_not_charging": make_entity_state_condition(
        BATTERY_CHARGING_DOMAIN_SPECS, STATE_OFF
    ),
    "is_level": make_entity_numerical_condition(
        BATTERY_PERCENTAGE_DOMAIN_SPECS, PERCENTAGE
    ),
}


async def async_get_conditions(hass: HomeAssistant) -> dict[str, type[Condition]]:
    """Return the conditions for batteries."""
    return CONDITIONS
