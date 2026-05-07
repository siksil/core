"""The tests for the litejet component."""

from inpui.components import litejet
from inpui.components.litejet.const import DOMAIN
from inpui.core import HomeAssistant
from inpui.setup import async_setup_component

from . import async_init_integration


async def test_setup_with_no_config(hass: HomeAssistant) -> None:
    """Test that nothing happens."""
    assert await async_setup_component(hass, DOMAIN, {}) is True
    assert DOMAIN not in hass.data


async def test_unload_entry(hass: HomeAssistant, mock_litejet) -> None:
    """Test being able to unload an entry."""
    entry = await async_init_integration(hass, use_switch=True, use_scene=True)

    assert await litejet.async_unload_entry(hass, entry)
    assert DOMAIN not in hass.data
