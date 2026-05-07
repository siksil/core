"""The nsw_fuel_station component."""

from __future__ import annotations

from nsw_fuel import FuelCheckClient

from inpui.core import HomeAssistant
from inpui.helpers import config_validation as cv
from inpui.helpers.typing import ConfigType

from .const import DATA_NSW_FUEL_STATION
from .coordinator import NSWFuelStationCoordinator

DOMAIN = "nsw_fuel_station"

CONFIG_SCHEMA = cv.platform_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the NSW Fuel Station platform."""
    client = FuelCheckClient()

    coordinator = NSWFuelStationCoordinator(hass, client)
    hass.data[DATA_NSW_FUEL_STATION] = coordinator

    await coordinator.async_refresh()

    return True
