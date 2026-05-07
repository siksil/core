"""Test for the smhi weather entity."""

import pytest
from syrupy.assertion import SnapshotAssertion

from inpui.const import Platform
from inpui.core import HomeAssistant
from inpui.helpers.entity_registry import EntityRegistry

from tests.common import MockConfigEntry, snapshot_platform


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
@pytest.mark.parametrize(
    "load_platforms",
    [[Platform.SENSOR]],
)
async def test_sensor_setup(
    hass: HomeAssistant,
    entity_registry: EntityRegistry,
    load_int: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test for successfully setting up the smhi sensors."""

    await snapshot_platform(hass, entity_registry, snapshot, load_int.entry_id)
