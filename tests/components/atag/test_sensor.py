"""Tests for the Atag sensor platform."""

from inpui.components.atag.sensor import SENSORS
from inpui.core import HomeAssistant
from inpui.helpers import entity_registry as er

from . import UID, init_integration

from tests.test_util.aiohttp import AiohttpClientMocker


async def test_sensors(
    hass: HomeAssistant,
    aioclient_mock: AiohttpClientMocker,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test the creation of ATAG sensors."""
    entry = await init_integration(hass, aioclient_mock)

    for item in SENSORS:
        sensor_id = "_".join(f"sensor.atag_thermostat_{item}".lower().split())
        assert entity_registry.async_is_registered(sensor_id)
        entry = entity_registry.async_get(sensor_id)
        assert entry.unique_id in [f"{UID}-{v}" for v in SENSORS.values()]
