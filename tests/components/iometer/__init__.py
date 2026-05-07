"""Tests for the IOmeter integration."""

from unittest.mock import patch

from inpui.const import Platform
from inpui.core import HomeAssistant

from tests.common import MockConfigEntry


async def setup_platform(
    hass: HomeAssistant, config_entry: MockConfigEntry, platforms: list[Platform]
) -> None:
    """Fixture for setting up the IOmeter platform."""
    config_entry.add_to_hass(hass)

    with patch("inpui.components.iometer.PLATFORMS", platforms):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
