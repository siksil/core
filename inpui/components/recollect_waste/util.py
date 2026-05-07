"""Define ReCollect Waste utilities."""

from aiorecollect.client import PickupType

from inpui.config_entries import ConfigEntry
from inpui.const import CONF_FRIENDLY_NAME
from inpui.core import callback


@callback
def async_get_pickup_type_names(
    entry: ConfigEntry, pickup_types: list[PickupType]
) -> list[str]:
    """Return proper pickup type names from their associated objects."""
    return [
        t.friendly_name
        if entry.options.get(CONF_FRIENDLY_NAME) and t.friendly_name
        else t.name
        for t in pickup_types
    ]
