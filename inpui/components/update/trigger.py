"""Provides triggers for update platform."""

from inpui.const import STATE_ON
from inpui.core import HomeAssistant
from inpui.helpers.trigger import Trigger, make_entity_target_state_trigger

from .const import DOMAIN

TRIGGERS: dict[str, type[Trigger]] = {
    "update_became_available": make_entity_target_state_trigger(DOMAIN, STATE_ON),
}


async def async_get_triggers(hass: HomeAssistant) -> dict[str, type[Trigger]]:
    """Return the triggers for update platform."""
    return TRIGGERS
