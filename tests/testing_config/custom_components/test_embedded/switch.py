"""Switch platform for the embedded component."""

from inpui.core import HomeAssistant
from inpui.helpers.entity_platform import AddEntitiesCallback
from inpui.helpers.typing import ConfigType, DiscoveryInfoType


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities_callback: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Find and return test switches."""
