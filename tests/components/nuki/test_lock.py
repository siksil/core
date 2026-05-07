"""Tests for the nuki locks."""

from unittest.mock import patch

import requests_mock
from syrupy.assertion import SnapshotAssertion

from inpui.const import Platform
from inpui.core import HomeAssistant
from inpui.helpers import entity_registry as er

from . import init_integration

from tests.common import snapshot_platform


async def test_locks(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_nuki_requests: requests_mock.Mocker,
) -> None:
    """Test locks."""
    with patch("inpui.components.nuki.PLATFORMS", [Platform.LOCK]):
        entry = await init_integration(hass, mock_nuki_requests)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
