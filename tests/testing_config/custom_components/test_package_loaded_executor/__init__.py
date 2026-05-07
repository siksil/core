"""Provide a mock package component."""

from inpui.core import HomeAssistant
from inpui.helpers.typing import ConfigType

from .const import TEST  # noqa: F401

DOMAIN = "test_package"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Mock a successful setup."""
    return True
