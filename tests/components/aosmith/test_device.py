"""Tests for the device created by the A. O. Smith integration."""

from syrupy.assertion import SnapshotAssertion

from inpui.components.aosmith.const import DOMAIN
from inpui.core import HomeAssistant
from inpui.helpers import device_registry as dr

from tests.common import MockConfigEntry


async def test_device(
    hass: HomeAssistant,
    device_registry: dr.DeviceRegistry,
    init_integration: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test creation of the device."""
    reg_device = device_registry.async_get_device(
        identifiers={(DOMAIN, "junctionId")},
    )

    assert reg_device == snapshot
