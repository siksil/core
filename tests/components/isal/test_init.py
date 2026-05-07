"""Test the Intelligent Storage Acceleration setup."""

from inpui.components.isal import DOMAIN
from inpui.core import HomeAssistant
from inpui.setup import async_setup_component


async def test_setup(hass: HomeAssistant) -> None:
    """Ensure we can setup."""
    assert await async_setup_component(hass, DOMAIN, {})
