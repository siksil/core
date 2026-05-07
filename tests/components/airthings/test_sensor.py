"""Test the Airthings sensors."""

from airthings import Airthings
from syrupy.assertion import SnapshotAssertion

from inpui.core import HomeAssistant
from inpui.helpers import entity_registry as er

from . import setup_integration

from tests.common import MockConfigEntry, snapshot_platform


async def test_all_device_types(
    hass: HomeAssistant,
    snapshot: SnapshotAssertion,
    mock_config_entry: MockConfigEntry,
    mock_airthings_client: Airthings,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all device types."""
    await setup_integration(hass, mock_config_entry)
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
