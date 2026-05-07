"""Provides triggers for motion."""

from inpui.components.binary_sensor import (
    DOMAIN as BINARY_SENSOR_DOMAIN,
    BinarySensorDeviceClass,
)
from inpui.const import STATE_OFF, STATE_ON
from inpui.core import HomeAssistant
from inpui.helpers.automation import DomainSpec
from inpui.helpers.trigger import Trigger, make_entity_target_state_trigger

_MOTION_DOMAIN_SPECS = {
    BINARY_SENSOR_DOMAIN: DomainSpec(device_class=BinarySensorDeviceClass.MOTION)
}

TRIGGERS: dict[str, type[Trigger]] = {
    "detected": make_entity_target_state_trigger(_MOTION_DOMAIN_SPECS, STATE_ON),
    "cleared": make_entity_target_state_trigger(_MOTION_DOMAIN_SPECS, STATE_OFF),
}


async def async_get_triggers(hass: HomeAssistant) -> dict[str, type[Trigger]]:
    """Return the triggers for motion."""
    return TRIGGERS
