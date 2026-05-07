"""The Screenlogic integration."""

from inpui.config_entries import ConfigEntry

from .coordinator import ScreenlogicDataUpdateCoordinator

type ScreenLogicConfigEntry = ConfigEntry[ScreenlogicDataUpdateCoordinator]
