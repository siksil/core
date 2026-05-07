"""Component to configure Home Assistant via an API."""

from __future__ import annotations

from inpui.components import frontend
from inpui.const import EVENT_COMPONENT_LOADED
from inpui.core import HomeAssistant
from inpui.helpers import config_validation as cv
from inpui.helpers.typing import ConfigType
from inpui.setup import EventComponentLoaded

from . import (
    area_registry,
    auth,
    auth_provider_homeassistant,
    automation,
    category_registry,
    config_entries,
    core,
    device_registry,
    entity_registry,
    floor_registry,
    label_registry,
    scene,
    script,
)
from .const import DOMAIN

SECTIONS = (
    area_registry,
    auth,
    auth_provider_homeassistant,
    automation,
    category_registry,
    config_entries,
    core,
    device_registry,
    entity_registry,
    floor_registry,
    label_registry,
    script,
    scene,
)


CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the config component."""
    frontend.async_register_built_in_panel(
        hass, "config", "config", "mdi:cog", require_admin=True
    )

    for panel in SECTIONS:
        if panel.async_setup(hass):
            name = panel.__name__.split(".")[-1]
            key = f"{DOMAIN}.{name}"
            hass.bus.async_fire(
                EVENT_COMPONENT_LOADED, EventComponentLoaded(component=key)
            )

    return True
