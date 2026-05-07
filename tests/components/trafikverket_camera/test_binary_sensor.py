"""The test for the Trafikverket binary sensor platform."""

from __future__ import annotations

import pytest
from pytrafikverket import CameraInfoModel

from inpui.config_entries import ConfigEntry
from inpui.const import STATE_ON
from inpui.core import HomeAssistant


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensor(
    hass: HomeAssistant,
    load_int: ConfigEntry,
    get_camera: CameraInfoModel,
) -> None:
    """Test the Trafikverket Camera binary sensor."""

    state = hass.states.get("binary_sensor.test_camera_active")
    assert state.state == STATE_ON
