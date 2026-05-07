"""Describe homeassistant logbook events."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from inpui.components.logbook import (
    LOGBOOK_ENTRY_ICON,
    LOGBOOK_ENTRY_MESSAGE,
    LOGBOOK_ENTRY_NAME,
)
from inpui.const import EVENT_INPUI_START, EVENT_INPUI_STOP
from inpui.core import Event, HomeAssistant, callback
from inpui.helpers.typing import NoEventData
from inpui.util.event_type import EventType

from .const import DOMAIN

EVENT_TO_NAME: dict[EventType[Any] | str, str] = {
    EVENT_INPUI_STOP: "stopped",
    EVENT_INPUI_START: "started",
}


@callback
def async_describe_events(
    hass: HomeAssistant,
    async_describe_event: Callable[
        [str, EventType[NoEventData] | str, Callable[[Event], dict[str, str]]], None
    ],
) -> None:
    """Describe logbook events."""

    @callback
    def async_describe_hass_event(event: Event[NoEventData]) -> dict[str, str]:
        """Describe homeassistant logbook event."""
        return {
            LOGBOOK_ENTRY_NAME: "Home Assistant",
            LOGBOOK_ENTRY_MESSAGE: EVENT_TO_NAME[event.event_type],
            LOGBOOK_ENTRY_ICON: "mdi:home-assistant",
        }

    async_describe_event(DOMAIN, EVENT_INPUI_STOP, async_describe_hass_event)
    async_describe_event(DOMAIN, EVENT_INPUI_START, async_describe_hass_event)
