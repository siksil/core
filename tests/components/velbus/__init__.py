"""Tests for the Velbus component."""

from inpui.components.velbus import VelbusConfigEntry
from inpui.core import HomeAssistant


async def init_integration(
    hass: HomeAssistant,
    config_entry: VelbusConfigEntry,
) -> None:
    """Load the Velbus integration."""
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
