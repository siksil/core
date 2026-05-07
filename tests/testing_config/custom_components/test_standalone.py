"""Provide a mock standalone component."""

from inpui.core import HomeAssistant
from inpui.helpers.typing import ConfigType

DOMAIN = "test_standalone"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Mock a successful setup."""
    return True
