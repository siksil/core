"""Integration for motion triggers."""

from __future__ import annotations

from inpui.core import HomeAssistant
from inpui.helpers import config_validation as cv
from inpui.helpers.typing import ConfigType

DOMAIN = "motion"
CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

__all__ = []


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the component."""
    return True
