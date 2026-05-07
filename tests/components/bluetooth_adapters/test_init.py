"""Test the Bluetooth Adapters setup."""

from inpui.components.bluetooth_adapters import DOMAIN
from inpui.core import HomeAssistant
from inpui.setup import async_setup_component


async def test_setup(hass: HomeAssistant) -> None:
    """Ensure we can setup."""
    assert await async_setup_component(hass, DOMAIN, {})
