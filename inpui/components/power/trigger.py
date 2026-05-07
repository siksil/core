"""Provides triggers for power."""

from __future__ import annotations

from inpui.components.sensor import DOMAIN as SENSOR_DOMAIN, SensorDeviceClass
from inpui.const import UnitOfPower
from inpui.core import HomeAssistant
from inpui.helpers.automation import DomainSpec
from inpui.helpers.trigger import (
    Trigger,
    make_entity_numerical_state_changed_with_unit_trigger,
    make_entity_numerical_state_crossed_threshold_with_unit_trigger,
)
from inpui.util.unit_conversion import PowerConverter

POWER_DOMAIN_SPECS: dict[str, DomainSpec] = {
    SENSOR_DOMAIN: DomainSpec(device_class=SensorDeviceClass.POWER),
}


TRIGGERS: dict[str, type[Trigger]] = {
    "changed": make_entity_numerical_state_changed_with_unit_trigger(
        POWER_DOMAIN_SPECS, UnitOfPower.WATT, PowerConverter
    ),
    "crossed_threshold": make_entity_numerical_state_crossed_threshold_with_unit_trigger(
        POWER_DOMAIN_SPECS, UnitOfPower.WATT, PowerConverter
    ),
}


async def async_get_triggers(hass: HomeAssistant) -> dict[str, type[Trigger]]:
    """Return the triggers for power."""
    return TRIGGERS
