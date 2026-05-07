"""Device automation exceptions."""

from inpui.exceptions import HomeAssistantError


class InvalidDeviceAutomationConfig(HomeAssistantError):
    """When device automation config is invalid."""


class DeviceNotFound(HomeAssistantError):
    """When referenced device not found."""


class EntityNotFound(HomeAssistantError):
    """When referenced entity not found."""
