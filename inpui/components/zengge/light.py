"""Support for Zengge lights."""

from __future__ import annotations

import voluptuous as vol

from inpui.components.light import PLATFORM_SCHEMA as LIGHT_PLATFORM_SCHEMA
from inpui.const import CONF_DEVICES, CONF_NAME
from inpui.core import HomeAssistant
from inpui.helpers import config_validation as cv, issue_registry as ir
from inpui.helpers.entity_platform import AddEntitiesCallback
from inpui.helpers.typing import ConfigType, DiscoveryInfoType

DEVICE_SCHEMA = vol.Schema({vol.Optional(CONF_NAME): cv.string})
DOMAIN = "zengge"

PLATFORM_SCHEMA = LIGHT_PLATFORM_SCHEMA.extend(
    {vol.Optional(CONF_DEVICES, default={}): {cv.string: DEVICE_SCHEMA}}
)


def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Zengge platform."""
    ir.async_create_issue(
        hass,
        DOMAIN,
        DOMAIN,
        is_fixable=False,
        severity=ir.IssueSeverity.ERROR,
        translation_key="integration_removed",
        translation_placeholders={
            "led_ble_url": "https://www.home-assistant.io/integrations/led_ble/",
        },
    )
