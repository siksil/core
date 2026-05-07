"""The Open Thread Border Router integration types."""

from inpui.config_entries import ConfigEntry

from .util import OTBRData

type OTBRConfigEntry = ConfigEntry[OTBRData]
