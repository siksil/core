"""Provides triggers for sirens."""

from inpui.const import STATE_OFF, STATE_ON
from inpui.core import HomeAssistant
from inpui.helpers.trigger import Trigger, make_entity_target_state_trigger

from . import DOMAIN

TRIGGERS: dict[str, type[Trigger]] = {
    "turned_on": make_entity_target_state_trigger(DOMAIN, STATE_ON),
    "turned_off": make_entity_target_state_trigger(DOMAIN, STATE_OFF),
}


async def async_get_triggers(hass: HomeAssistant) -> dict[str, type[Trigger]]:
    """Return the triggers for sirens."""
    return TRIGGERS
