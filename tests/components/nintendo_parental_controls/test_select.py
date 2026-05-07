"""Tests for Nintendo Switch Parental Controls select platform."""

from unittest.mock import AsyncMock, patch

from pynintendoparental.enum import DeviceTimerMode
from syrupy.assertion import SnapshotAssertion

from inpui.components.select import (
    ATTR_OPTION,
    DOMAIN as SELECT_DOMAIN,
    SERVICE_SELECT_OPTION,
)
from inpui.const import ATTR_ENTITY_ID, Platform
from inpui.core import HomeAssistant
from inpui.helpers import entity_registry as er

from . import setup_integration

from tests.common import MockConfigEntry, snapshot_platform


async def test_select(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_nintendo_client: AsyncMock,
    mock_nintendo_device: AsyncMock,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test select platform."""
    with patch(
        "homeassistant.components.nintendo_parental_controls._PLATFORMS",
        [Platform.SELECT],
    ):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_select_option(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_nintendo_client: AsyncMock,
    mock_nintendo_device: AsyncMock,
) -> None:
    """Test select option service."""
    with patch(
        "homeassistant.components.nintendo_parental_controls._PLATFORMS",
        [Platform.SELECT],
    ):
        await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        SELECT_DOMAIN,
        SERVICE_SELECT_OPTION,
        {
            ATTR_ENTITY_ID: "select.home_assistant_test_restriction_mode",
            ATTR_OPTION: DeviceTimerMode.EACH_DAY_OF_THE_WEEK.name.lower(),
        },
        blocking=True,
    )
    mock_nintendo_device.set_timer_mode.assert_awaited_once_with(
        DeviceTimerMode.EACH_DAY_OF_THE_WEEK
    )
