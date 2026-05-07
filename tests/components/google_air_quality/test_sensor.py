"""Test the Google Air Quality sensor."""

from unittest.mock import AsyncMock, patch

from syrupy.assertion import SnapshotAssertion

from inpui.config_entries import ConfigEntryState
from inpui.const import Platform
from inpui.core import HomeAssistant
from inpui.helpers import entity_registry as er

from tests.common import MockConfigEntry, snapshot_platform


async def test_sensor_snapshot(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
    mock_api: AsyncMock,
    snapshot: SnapshotAssertion,
) -> None:
    """Snapshot test of the sensors."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    assert mock_config_entry.state is ConfigEntryState.LOADED

    with patch(
        "inpui.components.google_air_quality.PLATFORMS",
        [Platform.SENSOR],
    ):
        await snapshot_platform(
            hass, entity_registry, snapshot, mock_config_entry.entry_id
        )
