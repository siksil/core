"""application_credentials platform for Geocaching."""

from inpui.components.application_credentials import ClientCredential
from inpui.core import HomeAssistant
from inpui.helpers import config_entry_oauth2_flow

from .oauth import GeocachingOAuth2Implementation


async def async_get_auth_implementation(
    hass: HomeAssistant, auth_domain: str, credential: ClientCredential
) -> config_entry_oauth2_flow.AbstractOAuth2Implementation:
    """Return auth implementation."""
    return GeocachingOAuth2Implementation(hass, auth_domain, credential)
