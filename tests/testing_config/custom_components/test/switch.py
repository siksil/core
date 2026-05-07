"""Stub switch platform for translation tests."""

from inpui.core import HomeAssistant
from inpui.helpers.entity_platform import AddEntitiesCallback
from inpui.helpers.typing import ConfigType, DiscoveryInfoType


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities_callback: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Stub setup for translation tests."""
    async_add_entities_callback([])
