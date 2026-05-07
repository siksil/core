"""Support for Qwikswitch relays."""

from __future__ import annotations

from inpui.components.switch import SwitchEntity
from inpui.core import HomeAssistant
from inpui.helpers.entity_platform import AddEntitiesCallback
from inpui.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DATA_QUIKSWITCH, DOMAIN
from .entity import QSToggleEntity


async def async_setup_platform(
    hass: HomeAssistant,
    _: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Add switches from the main Qwikswitch component."""
    if discovery_info is None:
        return

    qsusb = hass.data[DATA_QUIKSWITCH]
    devs = [QSSwitch(qsid, qsusb) for qsid in discovery_info[DOMAIN]]
    add_entities(devs)


class QSSwitch(QSToggleEntity, SwitchEntity):
    """Switch based on a Qwikswitch relay module."""
