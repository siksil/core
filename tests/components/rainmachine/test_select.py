"""Test RainMachine select entities."""

from typing import Any
from unittest.mock import AsyncMock, patch

from syrupy.assertion import SnapshotAssertion

from inpui.components.rainmachine import DOMAIN
from inpui.const import Platform
from inpui.core import HomeAssistant
from inpui.helpers import entity_registry as er
from inpui.setup import async_setup_component

from tests.common import MockConfigEntry, snapshot_platform


async def test_select_entities(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    config: dict[str, Any],
    config_entry: MockConfigEntry,
    client: AsyncMock,
) -> None:
    """Test select entities."""
    with (
        patch("inpui.components.rainmachine.Client", return_value=client),
        patch("inpui.components.rainmachine.PLATFORMS", [Platform.SELECT]),
    ):
        assert await async_setup_component(hass, DOMAIN, config)
        await hass.async_block_till_done()
    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)
