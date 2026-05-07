"""Provides conditions for fans."""

from inpui.const import STATE_OFF, STATE_ON
from inpui.core import HomeAssistant
from inpui.helpers.condition import Condition, make_entity_state_condition

from . import DOMAIN

CONDITIONS: dict[str, type[Condition]] = {
    "is_off": make_entity_state_condition(DOMAIN, STATE_OFF),
    "is_on": make_entity_state_condition(DOMAIN, STATE_ON),
}


async def async_get_conditions(hass: HomeAssistant) -> dict[str, type[Condition]]:
    """Return the fan conditions."""
    return CONDITIONS
