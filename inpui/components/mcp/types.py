"""Types for the Model Context Protocol integration."""

from inpui.config_entries import ConfigEntry

from .coordinator import ModelContextProtocolCoordinator

type ModelContextProtocolConfigEntry = ConfigEntry[ModelContextProtocolCoordinator]
