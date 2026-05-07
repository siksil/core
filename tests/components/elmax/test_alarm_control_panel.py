"""Tests for the Elmax alarm control panels."""

from datetime import timedelta
from unittest.mock import patch

from syrupy.assertion import SnapshotAssertion

from inpui.components.elmax.const import POLLING_SECONDS
from inpui.const import Platform
from inpui.core import HomeAssistant
from inpui.helpers import entity_registry as er

from . import init_integration

from tests.common import snapshot_platform

WAIT = timedelta(seconds=POLLING_SECONDS)


async def test_alarm_control_panels(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test alarm control panels."""
    with patch(
        "inpui.components.elmax.ELMAX_PLATFORMS", [Platform.ALARM_CONTROL_PANEL]
    ):
        entry = await init_integration(hass)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
