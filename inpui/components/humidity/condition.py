"""Provides conditions for humidity."""

from __future__ import annotations

from inpui.components.climate import (
    ATTR_CURRENT_HUMIDITY as CLIMATE_ATTR_CURRENT_HUMIDITY,
    DOMAIN as CLIMATE_DOMAIN,
)
from inpui.components.humidifier import (
    ATTR_CURRENT_HUMIDITY as HUMIDIFIER_ATTR_CURRENT_HUMIDITY,
    DOMAIN as HUMIDIFIER_DOMAIN,
)
from inpui.components.sensor import DOMAIN as SENSOR_DOMAIN, SensorDeviceClass
from inpui.components.weather import (
    ATTR_WEATHER_HUMIDITY,
    DOMAIN as WEATHER_DOMAIN,
)
from inpui.const import PERCENTAGE
from inpui.core import HomeAssistant
from inpui.helpers.automation import DomainSpec
from inpui.helpers.condition import Condition, make_entity_numerical_condition

HUMIDITY_DOMAIN_SPECS = {
    CLIMATE_DOMAIN: DomainSpec(
        value_source=CLIMATE_ATTR_CURRENT_HUMIDITY,
    ),
    HUMIDIFIER_DOMAIN: DomainSpec(
        value_source=HUMIDIFIER_ATTR_CURRENT_HUMIDITY,
    ),
    SENSOR_DOMAIN: DomainSpec(device_class=SensorDeviceClass.HUMIDITY),
    WEATHER_DOMAIN: DomainSpec(
        value_source=ATTR_WEATHER_HUMIDITY,
    ),
}

CONDITIONS: dict[str, type[Condition]] = {
    "is_value": make_entity_numerical_condition(HUMIDITY_DOMAIN_SPECS, PERCENTAGE),
}


async def async_get_conditions(hass: HomeAssistant) -> dict[str, type[Condition]]:
    """Return the conditions for humidity."""
    return CONDITIONS
