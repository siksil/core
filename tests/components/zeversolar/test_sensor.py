"""Test the sensor classes."""

from unittest.mock import patch

from syrupy.assertion import SnapshotAssertion

from inpui.const import Platform
from inpui.core import HomeAssistant
from inpui.helpers import entity_registry as er

from . import init_integration

from tests.common import snapshot_platform


async def test_sensors(
    hass: HomeAssistant, entity_registry: er.EntityRegistry, snapshot: SnapshotAssertion
) -> None:
    """Test sensors."""

    with patch(
        "homeassistant.components.zeversolar.PLATFORMS",
        [Platform.SENSOR],
    ):
        entry = await init_integration(hass)

        await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
