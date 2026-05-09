"""
Inpui Cloud Compatibility Stub.

This module provides a minimal API surface that mimics the original 'cloud'
(Nabu Casa) integration. It is used to prevent failures in core integrations
(like mobile_app, netatmo, etc.) that still expect the 'cloud' component
to be present for certain features like remote UI URLs or cloudhooks.
"""

from __future__ import annotations

from enum import StrEnum
import logging
from typing import Any

from inpui.core import HomeAssistant, callback

_LOGGER = logging.getLogger(__name__)
DOMAIN = "cloud"

class CloudConnectionState(StrEnum):
    """Cloud connection states."""
    CLOUD_CONNECTED = "connected"
    CLOUD_DISCONNECTED = "disconnected"

class CloudNotAvailable(Exception):
    """Exception to raise when cloud is not available."""

@callback
def async_is_logged_in(hass: HomeAssistant) -> bool:
    """Return if the user is logged in to the cloud."""
    # We return False by default to avoid integrations trying to use 
    # Nabu Casa specific features.
    return False

@callback
def async_active_subscription(hass: HomeAssistant) -> bool:
    """Return if the user has an active subscription."""
    return False

@callback
def async_is_connected(hass: HomeAssistant) -> bool:
    """Return if the cloud is connected."""
    # If the user has inpui_cloud set up and running, we might consider returning True here
    # but for now, we keep it simple.
    return False

async def async_remote_ui_url(hass: HomeAssistant) -> str:
    """Return the remote UI URL."""
    raise CloudNotAvailable("Inpui Cloud is active, but Nabu Casa remote UI is not used.")

async def async_delete_cloudhook(hass: HomeAssistant, webhook_id: str) -> None:
    """Delete a cloudhook."""
    pass

@callback
def async_listen_connection_change(hass: HomeAssistant, callback_func: Any) -> Any:
    """Listen for connection changes."""
    return lambda: None

@callback
def async_listen_cloudhook_change(hass: HomeAssistant, webhook_id: str, callback_func: Any) -> Any:
    """Listen for cloudhook changes."""
    return lambda: None

async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up the cloud stub."""
    _LOGGER.info("Inpui Cloud Compatibility Stub initialized.")
    return True
