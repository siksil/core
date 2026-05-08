"""Config flow for Inpui Cloud — pairing code entry."""

import uuid
import logging

import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, CONF_PAIRING_CODE, CONF_HUB_ID, CONF_JWT_TOKEN, CONF_TUNNEL_TOKEN, CONF_REMOTE_URL
from .api import InpuiCloudAPI

_LOGGER = logging.getLogger(__name__)


def _get_hardware_uuid() -> str:
    """
    Generate a persistent, unique hardware UUID for this installation.
    Uses uuid.getnode() which returns the MAC address as a 48-bit int,
    creating a deterministic ID per physical device.
    """
    node = uuid.getnode()
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"aeondeck-{node}"))


class InpuiCloudConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Inpui Cloud."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            hw_uuid = _get_hardware_uuid()

            api = InpuiCloudAPI()
            try:
                result = await api.pair_device(
                    pairing_code=user_input[CONF_PAIRING_CODE],
                    hw_uuid=hw_uuid,
                )
                # Map from API response keys to our config entry keys
                entry_data = {
                    CONF_HUB_ID: result["hub_id"],
                    CONF_JWT_TOKEN: result["jwt"],
                    CONF_TUNNEL_TOKEN: result["tunnel_token"],
                    CONF_REMOTE_URL: result["remote_url"],
                }
                return self.async_create_entry(
                    title="Inpui Cloud",
                    data=entry_data,
                )
            except Exception:
                _LOGGER.exception("Failed to pair with Inpui Cloud")
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PAIRING_CODE): str,
                }
            ),
            errors=errors,
        )
