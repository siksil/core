"""The Home Assistant Hardware integration."""

from __future__ import annotations

from inpui.core import HomeAssistant
from inpui.helpers import config_validation as cv
from inpui.helpers.typing import ConfigType

from .const import DATA_COMPONENT, DOMAIN
from .helpers import HardwareInfoDispatcher

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the component."""

    hass.data[DATA_COMPONENT] = HardwareInfoDispatcher(hass)

    return True
