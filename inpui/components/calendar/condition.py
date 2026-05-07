"""Provides conditions for calendars."""

from inpui.const import STATE_ON
from inpui.core import HomeAssistant
from inpui.helpers.condition import Condition, make_entity_state_condition

from .const import DOMAIN

CONDITIONS: dict[str, type[Condition]] = {
    "is_event_active": make_entity_state_condition(DOMAIN, STATE_ON),
}


async def async_get_conditions(hass: HomeAssistant) -> dict[str, type[Condition]]:
    """Return the calendar conditions."""
    return CONDITIONS
