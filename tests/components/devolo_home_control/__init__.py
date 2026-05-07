"""Tests for the devolo_home_control integration."""

from inpui.components.devolo_home_control.const import DOMAIN
from inpui.core import HomeAssistant

from tests.common import MockConfigEntry


def configure_integration(hass: HomeAssistant) -> MockConfigEntry:
    """Configure the integration."""
    config = {
        "username": "test-username",
        "password": "test-password",
    }
    entry = MockConfigEntry(
        domain=DOMAIN, data=config, entry_id="123456", unique_id="123456"
    )
    entry.add_to_hass(hass)

    return entry
