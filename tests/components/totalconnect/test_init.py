"""Tests for the TotalConnect init process."""

from unittest.mock import patch

from total_connect_client.exceptions import AuthenticationError

from inpui.config_entries import ConfigEntryState
from inpui.core import HomeAssistant

from . import setup_integration

from tests.common import MockConfigEntry


async def test_reauth_start(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that reauth is started when we have login errors."""
    with patch(
        "inpui.components.totalconnect.TotalConnectClient",
    ) as mock_client:
        mock_client.side_effect = AuthenticationError()
        await setup_integration(hass, mock_config_entry)

    assert mock_config_entry.state is ConfigEntryState.SETUP_ERROR
