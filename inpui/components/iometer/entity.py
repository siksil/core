"""Base class for IOmeter entities."""

from inpui.const import CONF_HOST
from inpui.helpers.device_registry import DeviceInfo
from inpui.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import IOMeterCoordinator


class IOmeterEntity(CoordinatorEntity[IOMeterCoordinator]):
    """Defines a base IOmeter entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: IOMeterCoordinator) -> None:
        """Initialize IOmeter entity."""
        super().__init__(coordinator)
        status = coordinator.data.status
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, status.device.id)},
            manufacturer="IOmeter GmbH",
            model="IOmeter",
            sw_version=coordinator.current_fw_version,
            configuration_url=f"http://{coordinator.config_entry.data[CONF_HOST]}/",
        )
