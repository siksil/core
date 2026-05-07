"""Tests for the Genius Hub component."""

from unittest.mock import AsyncMock

from inpui.components.geniushub import DOMAIN
from inpui.components.sensor import DOMAIN as SENSOR_DOMAIN
from inpui.const import CONF_MAC, CONF_TOKEN
from inpui.core import HomeAssistant
from inpui.helpers import entity_registry as er

from tests.common import MockConfigEntry


async def test_cloud_unique_id_migration(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    mock_geniushub_cloud: AsyncMock,
) -> None:
    """Test that the cloud unique ID is migrated to the entry_id."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Genius hub",
        data={
            CONF_TOKEN: "abcdef",
            CONF_MAC: "aa:bb:cc:dd:ee:ff",
        },
        entry_id="1234",
    )
    entry.add_to_hass(hass)
    entity_registry.async_get_or_create(
        SENSOR_DOMAIN, DOMAIN, "aa:bb:cc:dd:ee:ff_device_78", config_entry=entry
    )
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert hass.states.get("sensor.geniushub_aa_bb_cc_dd_ee_ff_device_78")
    entity_entry = entity_registry.async_get(
        "sensor.geniushub_aa_bb_cc_dd_ee_ff_device_78"
    )
    assert entity_entry.unique_id == "1234_device_78"
