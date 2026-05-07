"""Test fixtures for the Plaato integration."""

from collections.abc import AsyncGenerator
from unittest.mock import patch

from pyplaato.models.airlock import PlaatoAirlock
from pyplaato.models.device import PlaatoDeviceType
from pyplaato.models.keg import PlaatoKeg
import pytest

from inpui.components.plaato.const import (
    CONF_DEVICE_NAME,
    CONF_DEVICE_TYPE,
    CONF_USE_WEBHOOK,
    DOMAIN,
)
from inpui.const import CONF_TOKEN, Platform
from inpui.core import HomeAssistant

from tests.common import MockConfigEntry

# Note: It would be good to replace this test data
# with actual data from the API
AIRLOCK_DATA = {}
KEG_DATA = {}


@pytest.fixture
async def init_integration(
    hass: HomeAssistant,
    device_type: PlaatoDeviceType,
    platform: Platform,
) -> AsyncGenerator[MockConfigEntry]:
    """Mock integration setup."""
    with (
        patch(
            "inpui.components.plaato.PLATFORMS",
            [platform],
        ),
        patch(
            "inpui.components.plaato.coordinator.Plaato.get_airlock_data",
            return_value=PlaatoAirlock(AIRLOCK_DATA),
        ),
        patch(
            "inpui.components.plaato.coordinator.Plaato.get_keg_data",
            return_value=PlaatoKeg(KEG_DATA),
        ),
    ):
        entry = MockConfigEntry(
            domain=DOMAIN,
            data={
                CONF_USE_WEBHOOK: False,
                CONF_TOKEN: "valid_token",
                CONF_DEVICE_TYPE: device_type,
                CONF_DEVICE_NAME: "device_name",
            },
            entry_id="123456",
        )
        entry.add_to_hass(hass)
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        yield entry
