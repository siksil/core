"""Tests for the Omnilogic integration."""

from unittest.mock import patch

from inpui.components.omnilogic.const import DOMAIN
from inpui.const import CONF_PASSWORD, CONF_USERNAME
from inpui.core import HomeAssistant

from .const import TELEMETRY

from tests.common import MockConfigEntry


async def init_integration(hass: HomeAssistant) -> MockConfigEntry:
    """Mock integration setup."""
    with (
        patch(
            "inpui.components.omnilogic.OmniLogic.connect",
            return_value=True,
        ),
        patch(
            "inpui.components.omnilogic.OmniLogic.get_telemetry_data",
            return_value={},
        ),
        patch(
            "inpui.components.omnilogic.coordinator.OmniLogicUpdateCoordinator._async_update_data",
            return_value=TELEMETRY,
        ),
    ):
        entry = MockConfigEntry(
            domain=DOMAIN,
            data={CONF_USERNAME: "test-username", CONF_PASSWORD: "test-password"},
            entry_id="6fa019921cf8e7a3f57a3c2ed001a10d",
        )
        entry.add_to_hass(hass)
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        return entry
