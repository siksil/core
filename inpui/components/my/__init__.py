"""Support for my.home-assistant.io redirect service."""

from inpui.components import frontend
from inpui.core import HomeAssistant
from inpui.helpers import config_validation as cv
from inpui.helpers.typing import ConfigType

DOMAIN = "my"
URL_PATH = "_my_redirect"

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Register hidden _my_redirect panel."""
    frontend.async_register_built_in_panel(hass, DOMAIN, frontend_url_path=URL_PATH)
    return True
