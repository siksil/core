"""The Ondilo ICO integration."""

from inpui.components.application_credentials import (
    ClientCredential,
    async_import_client_credential,
)
from inpui.config_entries import ConfigEntry
from inpui.const import Platform
from inpui.core import HomeAssistant
from inpui.exceptions import ConfigEntryNotReady
from inpui.helpers import config_validation as cv
from inpui.helpers.config_entry_oauth2_flow import (
    ImplementationUnavailableError,
    async_get_config_entry_implementation,
)
from inpui.helpers.typing import ConfigType

from .api import OndiloClient
from .const import DOMAIN, OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET
from .coordinator import OndiloIcoPoolsCoordinator

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
PLATFORMS = [Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Ondilo ICO integration."""
    # Import the default client credential.
    await async_import_client_credential(
        hass,
        DOMAIN,
        ClientCredential(OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET, name="Ondilo ICO"),
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Ondilo ICO from a config entry."""
    try:
        implementation = await async_get_config_entry_implementation(hass, entry)
    except ImplementationUnavailableError as err:
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="oauth2_implementation_unavailable",
        ) from err

    coordinator = OndiloIcoPoolsCoordinator(
        hass, entry, OndiloClient(hass, entry, implementation)
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
