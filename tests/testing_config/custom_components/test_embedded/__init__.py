"""Component with embedded platforms."""

from inpui.core import HomeAssistant
from inpui.helpers.typing import ConfigType

DOMAIN = "test_embedded"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Mock config."""
    return True
