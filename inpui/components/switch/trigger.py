"""Provides triggers for switch platform."""

from inpui.components.input_boolean import DOMAIN as INPUT_BOOLEAN_DOMAIN
from inpui.const import STATE_OFF, STATE_ON
from inpui.core import HomeAssistant
from inpui.helpers.automation import DomainSpec
from inpui.helpers.trigger import Trigger, make_entity_target_state_trigger

from .const import DOMAIN

SWITCH_DOMAIN_SPECS = {DOMAIN: DomainSpec(), INPUT_BOOLEAN_DOMAIN: DomainSpec()}

TRIGGERS: dict[str, type[Trigger]] = {
    "turned_on": make_entity_target_state_trigger(SWITCH_DOMAIN_SPECS, STATE_ON),
    "turned_off": make_entity_target_state_trigger(SWITCH_DOMAIN_SPECS, STATE_OFF),
}


async def async_get_triggers(hass: HomeAssistant) -> dict[str, type[Trigger]]:
    """Return the triggers for switch platform."""
    return TRIGGERS
