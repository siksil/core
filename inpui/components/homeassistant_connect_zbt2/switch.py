"""Home Assistant Connect ZBT-2 switch entities."""

from __future__ import annotations

import logging

from inpui.components.inpui_hardware.coordinator import (
    FirmwareUpdateCoordinator,
)
from inpui.components.inpui_hardware.switch import (
    BaseBetaFirmwareSwitch,
)
from inpui.core import HomeAssistant
from inpui.helpers.device_registry import DeviceInfo
from inpui.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import HomeAssistantConnectZBT2ConfigEntry
from .const import DOMAIN, HARDWARE_NAME, SERIAL_NUMBER

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: HomeAssistantConnectZBT2ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the switch platform for Home Assistant Connect ZBT-2."""
    async_add_entities(
        [BetaFirmwareSwitch(config_entry.runtime_data.coordinator, config_entry)]
    )


class BetaFirmwareSwitch(BaseBetaFirmwareSwitch):
    """Home Assistant Connect ZBT-2 beta firmware switch."""

    def __init__(
        self,
        coordinator: FirmwareUpdateCoordinator,
        config_entry: HomeAssistantConnectZBT2ConfigEntry,
    ) -> None:
        """Initialize the beta firmware switch."""
        super().__init__(coordinator, config_entry)

        serial_number = self._config_entry.data[SERIAL_NUMBER]

        self._attr_unique_id = f"{serial_number}_beta_firmware"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, serial_number)},
            name=f"{HARDWARE_NAME} ({serial_number})",
            model=HARDWARE_NAME,
            manufacturer="Nabu Casa",
            serial_number=serial_number,
        )
