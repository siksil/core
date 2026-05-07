"""Types for the MCP server integration."""

from inpui.config_entries import ConfigEntry

from .session import SessionManager

type MCPServerConfigEntry = ConfigEntry[SessionManager]
