"""Errors for the Media Player component."""

from inpui.exceptions import HomeAssistantError


class MediaPlayerException(HomeAssistantError):
    """Base class for Media Player exceptions."""


class BrowseError(MediaPlayerException):
    """Error while browsing."""


class SearchError(MediaPlayerException):
    """Error while searching."""
