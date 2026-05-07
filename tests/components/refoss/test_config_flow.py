"""Tests for the refoss Integration."""

from unittest.mock import AsyncMock, patch

from homeassistant import config_entries
from inpui.components.refoss.const import DOMAIN
from inpui.core import HomeAssistant
from inpui.data_entry_flow import FlowResultType

from . import FakeDiscovery, build_base_device_mock


@patch("inpui.components.refoss.config_flow.DISCOVERY_TIMEOUT", 0)
async def test_creating_entry_sets_up(
    hass: HomeAssistant, mock_setup_entry: AsyncMock
) -> None:
    """Test setting up refoss."""
    with (
        patch(
            "inpui.components.refoss.util.Discovery",
            return_value=FakeDiscovery(),
        ),
        patch(
            "inpui.components.refoss.bridge.async_build_base_device",
            return_value=build_base_device_mock(),
        ),
        patch(
            "inpui.components.refoss.switch.isinstance",
            return_value=True,
        ),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

        # Confirmation form
        assert result["type"] is FlowResultType.FORM

        result = await hass.config_entries.flow.async_configure(result["flow_id"], {})

        assert result["type"] is FlowResultType.CREATE_ENTRY

        await hass.async_block_till_done()

        assert len(mock_setup_entry.mock_calls) == 1


@patch("inpui.components.refoss.config_flow.DISCOVERY_TIMEOUT", 0)
async def test_creating_entry_has_no_devices(
    hass: HomeAssistant, mock_setup_entry: AsyncMock
) -> None:
    """Test setting up Refoss no devices."""
    with patch(
        "inpui.components.refoss.util.Discovery",
        return_value=FakeDiscovery(),
    ) as discovery:
        discovery.return_value.mock_devices = {}

        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

        # Confirmation form
        assert result["type"] is FlowResultType.FORM

        result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
        assert result["type"] is FlowResultType.ABORT

        await hass.async_block_till_done()

        assert len(mock_setup_entry.mock_calls) == 0
