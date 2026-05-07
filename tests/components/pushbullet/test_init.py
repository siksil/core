"""Test pushbullet integration."""

from unittest.mock import patch

from pushbullet import InvalidKeyError, PushbulletError

from inpui.components.pushbullet.const import DOMAIN
from inpui.config_entries import ConfigEntryState
from inpui.const import EVENT_INPUI_START
from inpui.core import HomeAssistant

from . import MOCK_CONFIG

from tests.common import MockConfigEntry


async def test_async_setup_entry_success(
    hass: HomeAssistant, requests_mock_fixture
) -> None:
    """Test pushbullet successful setup."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED

    with patch(
        "inpui.components.pushbullet.api.PushBulletNotificationProvider.start"
    ) as mock_start:
        hass.bus.async_fire(EVENT_INPUI_START)
        await hass.async_block_till_done()
        mock_start.assert_called_once()


async def test_setup_entry_failed_invalid_key(hass: HomeAssistant) -> None:
    """Test pushbullet failed setup due to invalid key."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)
    with patch(
        "inpui.components.pushbullet.PushBullet",
        side_effect=InvalidKeyError,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.SETUP_ERROR


async def test_setup_entry_failed_conn_error(hass: HomeAssistant) -> None:
    """Test pushbullet failed setup due to conn error."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)
    with patch(
        "inpui.components.pushbullet.PushBullet",
        side_effect=PushbulletError,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_async_unload_entry(hass: HomeAssistant, requests_mock_fixture) -> None:
    """Test pushbullet unload entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.NOT_LOADED
