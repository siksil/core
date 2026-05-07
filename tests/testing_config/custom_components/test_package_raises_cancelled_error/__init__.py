"""Provide a mock package component."""

import asyncio

from inpui.core import HomeAssistant
from inpui.helpers.typing import ConfigType


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Mock a successful setup."""
    asyncio.current_task().cancel()
    await asyncio.sleep(0)
