"""Support for Mycroft AI."""

import voluptuous as vol

from inpui.const import CONF_HOST, Platform
from inpui.core import HomeAssistant
from inpui.helpers import config_validation as cv, discovery
from inpui.helpers.typing import ConfigType

DOMAIN = "mycroft"

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema({vol.Required(CONF_HOST): cv.string})}, extra=vol.ALLOW_EXTRA
)


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Mycroft component."""
    hass.data[DOMAIN] = config[DOMAIN][CONF_HOST]
    discovery.load_platform(hass, Platform.NOTIFY, DOMAIN, {}, config)
    return True
