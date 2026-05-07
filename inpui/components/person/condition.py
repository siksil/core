"""Provides conditions for persons."""

from inpui.const import STATE_HOME, STATE_NOT_HOME
from inpui.core import HomeAssistant
from inpui.helpers.condition import Condition, make_entity_state_condition

from .const import DOMAIN

CONDITIONS: dict[str, type[Condition]] = {
    "is_home": make_entity_state_condition(DOMAIN, STATE_HOME),
    "is_not_home": make_entity_state_condition(DOMAIN, STATE_NOT_HOME),
}


async def async_get_conditions(hass: HomeAssistant) -> dict[str, type[Condition]]:
    """Return the conditions for persons."""
    return CONDITIONS
