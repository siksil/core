"""Provides triggers for batteries."""

from __future__ import annotations

from inpui.components.binary_sensor import (
    DOMAIN as BINARY_SENSOR_DOMAIN,
    BinarySensorDeviceClass,
)
from inpui.components.sensor import DOMAIN as SENSOR_DOMAIN, SensorDeviceClass
from inpui.const import STATE_OFF, STATE_ON
from inpui.core import HomeAssistant
from inpui.helpers.automation import DomainSpec
from inpui.helpers.trigger import (
    Trigger,
    make_entity_numerical_state_changed_trigger,
    make_entity_numerical_state_crossed_threshold_trigger,
    make_entity_target_state_trigger,
)

BATTERY_LOW_DOMAIN_SPECS: dict[str, DomainSpec] = {
    BINARY_SENSOR_DOMAIN: DomainSpec(device_class=BinarySensorDeviceClass.BATTERY),
}

BATTERY_CHARGING_DOMAIN_SPECS: dict[str, DomainSpec] = {
    BINARY_SENSOR_DOMAIN: DomainSpec(
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING
    ),
}

BATTERY_PERCENTAGE_DOMAIN_SPECS: dict[str, DomainSpec] = {
    SENSOR_DOMAIN: DomainSpec(device_class=SensorDeviceClass.BATTERY),
}

TRIGGERS: dict[str, type[Trigger]] = {
    "low": make_entity_target_state_trigger(BATTERY_LOW_DOMAIN_SPECS, STATE_ON),
    "not_low": make_entity_target_state_trigger(BATTERY_LOW_DOMAIN_SPECS, STATE_OFF),
    "started_charging": make_entity_target_state_trigger(
        BATTERY_CHARGING_DOMAIN_SPECS, STATE_ON
    ),
    "stopped_charging": make_entity_target_state_trigger(
        BATTERY_CHARGING_DOMAIN_SPECS, STATE_OFF
    ),
    "level_changed": make_entity_numerical_state_changed_trigger(
        BATTERY_PERCENTAGE_DOMAIN_SPECS, valid_unit="%"
    ),
    "level_crossed_threshold": make_entity_numerical_state_crossed_threshold_trigger(
        BATTERY_PERCENTAGE_DOMAIN_SPECS, valid_unit="%"
    ),
}


async def async_get_triggers(hass: HomeAssistant) -> dict[str, type[Trigger]]:
    """Return the triggers for batteries."""
    return TRIGGERS
