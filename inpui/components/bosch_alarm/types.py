"""Types for the Bosch Alarm integration."""

from bosch_alarm_mode2 import Panel

from inpui.config_entries import ConfigEntry

type BoschAlarmConfigEntry = ConfigEntry[Panel]
