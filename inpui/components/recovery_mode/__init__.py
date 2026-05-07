"""The Recovery Mode integration."""

from inpui.components import persistent_notification
from inpui.core import HomeAssistant
from inpui.helpers import config_validation as cv
from inpui.helpers.typing import ConfigType

DOMAIN = "recovery_mode"

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Recovery Mode component."""
    persistent_notification.async_create(
        hass,
        (
            "Home Assistant is running in recovery mode. Check [the error"
            " log](/config/logs) to see what went wrong."
        ),
        "Recovery Mode",
    )
    return True
