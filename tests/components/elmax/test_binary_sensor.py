"""Tests for the Elmax binary sensors."""

from unittest.mock import patch

from syrupy.assertion import SnapshotAssertion

from inpui.const import Platform
from inpui.core import HomeAssistant
from inpui.helpers import entity_registry as er

from . import init_integration

from tests.common import snapshot_platform


async def test_binary_sensors(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test binary sensors."""
    with patch(
        "inpui.components.elmax.ELMAX_PLATFORMS", [Platform.BINARY_SENSOR]
    ):
        entry = await init_integration(hass)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
