"""WebSocket API related errors."""

from inpui.exceptions import HomeAssistantError


class Disconnect(HomeAssistantError):
    """Disconnect the current session."""
