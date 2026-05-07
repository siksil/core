"""The Eight Sleep integration config flow."""

from inpui.config_entries import ConfigFlow

from . import DOMAIN


class EightSleepConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Eight Sleep."""

    VERSION = 1
