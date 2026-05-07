"""The tests for Alarm control panel platforms."""

from inpui.config_entries import ConfigEntry
from inpui.const import Platform
from inpui.core import HomeAssistant


async def help_async_setup_entry_init(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> bool:
    """Set up test config entry."""
    await hass.config_entries.async_forward_entry_setups(
        config_entry, [Platform.ALARM_CONTROL_PANEL]
    )
    return True


async def help_async_unload_entry(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> bool:
    """Unload test config emntry."""
    return await hass.config_entries.async_unload_platforms(
        config_entry, [Platform.ALARM_CONTROL_PANEL]
    )
