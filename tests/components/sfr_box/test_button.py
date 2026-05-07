"""Test the SFR Box buttons."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from sfrbox_api.exceptions import SFRBoxError
from syrupy.assertion import SnapshotAssertion

from inpui.components.button import DOMAIN as BUTTON_DOMAIN, SERVICE_PRESS
from inpui.config_entries import ConfigEntry
from inpui.const import ATTR_ENTITY_ID, Platform
from inpui.core import HomeAssistant
from inpui.exceptions import HomeAssistantError
from inpui.helpers import entity_registry as er

from tests.common import snapshot_platform

pytestmark = pytest.mark.usefixtures("system_get_info", "dsl_get_info", "wan_get_info")


@pytest.fixture(autouse=True)
def override_platforms() -> Generator[None]:
    """Override PLATFORMS_WITH_AUTH."""
    with (
        patch(
            "inpui.components.sfr_box.PLATFORMS_WITH_AUTH", [Platform.BUTTON]
        ),
        patch("inpui.components.sfr_box.coordinator.SFRBox.authenticate"),
    ):
        yield


async def test_buttons(
    hass: HomeAssistant,
    config_entry_with_auth: ConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test for SFR Box buttons."""
    await hass.config_entries.async_setup(config_entry_with_auth.entry_id)
    await hass.async_block_till_done()

    await snapshot_platform(
        hass, entity_registry, snapshot, config_entry_with_auth.entry_id
    )


async def test_reboot(hass: HomeAssistant, config_entry_with_auth: ConfigEntry) -> None:
    """Test for SFR Box reboot button."""
    await hass.config_entries.async_setup(config_entry_with_auth.entry_id)
    await hass.async_block_till_done()

    # Reboot success
    service_data = {ATTR_ENTITY_ID: "button.sfr_box_restart"}
    with patch(
        "inpui.components.sfr_box.button.SFRBox.system_reboot"
    ) as mock_action:
        await hass.services.async_call(
            BUTTON_DOMAIN, SERVICE_PRESS, service_data=service_data, blocking=True
        )

    assert len(mock_action.mock_calls) == 1
    assert mock_action.mock_calls[0][1] == ()

    # Reboot failed
    service_data = {ATTR_ENTITY_ID: "button.sfr_box_restart"}
    with (
        patch(
            "inpui.components.sfr_box.button.SFRBox.system_reboot",
            side_effect=SFRBoxError,
        ) as mock_action,
        pytest.raises(HomeAssistantError),
    ):
        await hass.services.async_call(
            BUTTON_DOMAIN, SERVICE_PRESS, service_data=service_data, blocking=True
        )

    assert len(mock_action.mock_calls) == 1
    assert mock_action.mock_calls[0][1] == ()
