"""Test the Nightscout config flow."""

from http import HTTPStatus
from unittest.mock import patch

from aiohttp import ClientConnectionError, ClientResponseError

from homeassistant import config_entries
from inpui.components.nightscout.const import DOMAIN
from inpui.components.nightscout.utils import hash_from_url
from inpui.const import CONF_URL
from inpui.core import HomeAssistant
from inpui.data_entry_flow import FlowResultType

from . import GLUCOSE_READINGS, SERVER_STATUS, SERVER_STATUS_STATUS_ONLY

from tests.common import MockConfigEntry

CONFIG = {CONF_URL: "https://some.url:1234"}


async def test_form(hass: HomeAssistant) -> None:
    """Test we get the user initiated form."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    with (
        _patch_glucose_readings(),
        _patch_server_status(),
        _patch_async_setup_entry() as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            CONFIG,
        )

        assert result2["type"] is FlowResultType.CREATE_ENTRY
        assert result2["title"] == SERVER_STATUS.name  # pylint: disable=maybe-no-member
        assert result2["data"] == CONFIG
        await hass.async_block_till_done()
        assert len(mock_setup_entry.mock_calls) == 1


async def test_user_form_cannot_connect(hass: HomeAssistant) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "inpui.components.nightscout.NightscoutAPI.get_server_status",
        side_effect=ClientConnectionError(),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_URL: "https://some.url:1234"},
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}


async def test_user_form_api_key_required(hass: HomeAssistant) -> None:
    """Test we handle an unauthorized error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with (
        patch(
            "inpui.components.nightscout.NightscoutAPI.get_server_status",
            return_value=SERVER_STATUS_STATUS_ONLY,
        ),
        patch(
            "inpui.components.nightscout.NightscoutAPI.get_sgvs",
            side_effect=ClientResponseError(None, None, status=HTTPStatus.UNAUTHORIZED),
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_URL: "https://some.url:1234"},
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "invalid_auth"}


async def test_user_form_unexpected_exception(hass: HomeAssistant) -> None:
    """Test we handle unexpected exception."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "inpui.components.nightscout.NightscoutAPI.get_server_status",
        side_effect=Exception(),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_URL: "https://some.url:1234"},
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}


async def test_user_form_duplicate(hass: HomeAssistant) -> None:
    """Test duplicate entries."""
    with _patch_glucose_readings(), _patch_server_status():
        unique_id = hash_from_url(CONFIG[CONF_URL])
        entry = MockConfigEntry(domain=DOMAIN, unique_id=unique_id)
        entry.add_to_hass(hass)

        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
            data=CONFIG,
        )
        assert result["type"] is FlowResultType.ABORT
        assert result["reason"] == "already_configured"


def _patch_async_setup_entry():
    return patch(
        "inpui.components.nightscout.async_setup_entry",
        return_value=True,
    )


def _patch_glucose_readings():
    return patch(
        "inpui.components.nightscout.NightscoutAPI.get_sgvs",
        return_value=GLUCOSE_READINGS,
    )


def _patch_server_status():
    return patch(
        "inpui.components.nightscout.NightscoutAPI.get_server_status",
        return_value=SERVER_STATUS,
    )
