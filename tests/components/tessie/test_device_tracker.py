"""Test the Tessie device tracker platform."""

from syrupy.assertion import SnapshotAssertion

from inpui.const import Platform
from inpui.core import HomeAssistant
from inpui.helpers import entity_registry as er

from .common import assert_entities, setup_platform


async def test_device_tracker(
    hass: HomeAssistant, snapshot: SnapshotAssertion, entity_registry: er.EntityRegistry
) -> None:
    """Tests that the device tracker entities are correct."""

    entry = await setup_platform(hass, [Platform.DEVICE_TRACKER])

    assert_entities(hass, entry.entry_id, entity_registry, snapshot)
