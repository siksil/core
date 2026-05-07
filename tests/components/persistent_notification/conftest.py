"""The tests for the persistent notification component."""

import pytest

from inpui.components import persistent_notification as pn
from inpui.core import HomeAssistant
from inpui.setup import async_setup_component


@pytest.fixture(autouse=True)
async def setup_integration(hass: HomeAssistant) -> None:
    """Set up persistent notification integration."""
    assert await async_setup_component(hass, pn.DOMAIN, {})
