"""Binary sensor platform for Inpui Cloud."""
from inpui.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from inpui.config_entries import ConfigEntry
from inpui.core import HomeAssistant
from inpui.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, BINARY_SENSOR_CONNECTED

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary sensor platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    tunnel = data["tunnel"]
    
    async_add_entities([InpuiCloudTunnelSensor(tunnel, entry.entry_id)])

class InpuiCloudTunnelSensor(BinarySensorEntity):
    """Representation of the Inpui Cloud tunnel connection status."""

    _attr_has_entity_name = True
    _attr_name = "Cloud Connection"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_should_poll = True

    def __init__(self, tunnel, entry_id):
        """Initialize the sensor."""
        self._tunnel = tunnel
        self._attr_unique_id = f"{entry_id}_cloud_connection"

    @property
    def is_on(self) -> bool:
        """Return true if the tunnel is running."""
        return self._tunnel.proc is not None and self._tunnel.proc.returncode is None
