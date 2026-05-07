"""Analytics platform."""

from inpui.components.analytics import AnalyticsInput, AnalyticsModifications
from inpui.core import HomeAssistant


async def async_modify_analytics(
    hass: HomeAssistant, analytics_input: AnalyticsInput
) -> AnalyticsModifications:
    """Modify the analytics."""
    return AnalyticsModifications(remove=True)
