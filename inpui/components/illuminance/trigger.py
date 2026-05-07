"""Provides triggers for illuminance."""

from __future__ import annotations

from inpui.components.binary_sensor import (
    DOMAIN as BINARY_SENSOR_DOMAIN,
    BinarySensorDeviceClass,
)
from inpui.components.sensor import DOMAIN as SENSOR_DOMAIN, SensorDeviceClass
from inpui.const import LIGHT_LUX, STATE_OFF, STATE_ON
from inpui.core import HomeAssistant
from inpui.helpers.automation import DomainSpec
from inpui.helpers.trigger import (
    Trigger,
    make_entity_numerical_state_changed_trigger,
    make_entity_numerical_state_crossed_threshold_trigger,
    make_entity_target_state_trigger,
)

ILLUMINANCE_DOMAIN_SPECS: dict[str, DomainSpec] = {
    SENSOR_DOMAIN: DomainSpec(device_class=SensorDeviceClass.ILLUMINANCE),
}

TRIGGERS: dict[str, type[Trigger]] = {
    "detected": make_entity_target_state_trigger(
        {BINARY_SENSOR_DOMAIN: DomainSpec(device_class=BinarySensorDeviceClass.LIGHT)},
        STATE_ON,
    ),
    "cleared": make_entity_target_state_trigger(
        {BINARY_SENSOR_DOMAIN: DomainSpec(device_class=BinarySensorDeviceClass.LIGHT)},
        STATE_OFF,
    ),
    "changed": make_entity_numerical_state_changed_trigger(
        ILLUMINANCE_DOMAIN_SPECS, valid_unit=LIGHT_LUX
    ),
    "crossed_threshold": make_entity_numerical_state_crossed_threshold_trigger(
        ILLUMINANCE_DOMAIN_SPECS, valid_unit=LIGHT_LUX
    ),
}


async def async_get_triggers(hass: HomeAssistant) -> dict[str, type[Trigger]]:
    """Return the triggers for illuminance."""
    return TRIGGERS
