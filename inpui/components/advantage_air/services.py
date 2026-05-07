"""Services for Advantage Air integration."""

from __future__ import annotations

import voluptuous as vol

from inpui.components.sensor import DOMAIN as SENSOR_DOMAIN
from inpui.core import HomeAssistant, callback
from inpui.helpers import config_validation as cv, service

from .const import DOMAIN


@callback
def async_setup_services(hass: HomeAssistant) -> None:
    """Home Assistant services."""

    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        "set_time_to",
        entity_domain=SENSOR_DOMAIN,
        schema={vol.Required("minutes"): cv.positive_int},
        func="set_time_to",
    )
