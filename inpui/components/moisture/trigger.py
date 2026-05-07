"""Provides triggers for moisture."""

from __future__ import annotations

from inpui.components.binary_sensor import (
    DOMAIN as BINARY_SENSOR_DOMAIN,
    BinarySensorDeviceClass,
)
from inpui.components.sensor import DOMAIN as SENSOR_DOMAIN, SensorDeviceClass
from inpui.const import PERCENTAGE, STATE_OFF, STATE_ON
from inpui.core import HomeAssistant
from inpui.helpers.automation import DomainSpec
from inpui.helpers.trigger import (
    Trigger,
    make_entity_numerical_state_changed_trigger,
    make_entity_numerical_state_crossed_threshold_trigger,
    make_entity_target_state_trigger,
)

MOISTURE_BINARY_DOMAIN_SPECS: dict[str, DomainSpec] = {
    BINARY_SENSOR_DOMAIN: DomainSpec(device_class=BinarySensorDeviceClass.MOISTURE),
}

MOISTURE_NUMERICAL_DOMAIN_SPECS: dict[str, DomainSpec] = {
    SENSOR_DOMAIN: DomainSpec(device_class=SensorDeviceClass.MOISTURE),
}


TRIGGERS: dict[str, type[Trigger]] = {
    "detected": make_entity_target_state_trigger(
        MOISTURE_BINARY_DOMAIN_SPECS, STATE_ON
    ),
    "cleared": make_entity_target_state_trigger(
        MOISTURE_BINARY_DOMAIN_SPECS, STATE_OFF
    ),
    "changed": make_entity_numerical_state_changed_trigger(
        MOISTURE_NUMERICAL_DOMAIN_SPECS, valid_unit=PERCENTAGE
    ),
    "crossed_threshold": make_entity_numerical_state_crossed_threshold_trigger(
        MOISTURE_NUMERICAL_DOMAIN_SPECS, valid_unit=PERCENTAGE
    ),
}


async def async_get_triggers(hass: HomeAssistant) -> dict[str, type[Trigger]]:
    """Return the triggers for moisture."""
    return TRIGGERS
