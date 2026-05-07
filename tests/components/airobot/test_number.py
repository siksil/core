"""Test the Airobot number platform."""

from unittest.mock import AsyncMock

from pyairobotrest.exceptions import AirobotError
import pytest
from syrupy.assertion import SnapshotAssertion

from inpui.components.number import (
    ATTR_VALUE,
    DOMAIN as NUMBER_DOMAIN,
    SERVICE_SET_VALUE,
)
from inpui.const import ATTR_ENTITY_ID, Platform
from inpui.core import HomeAssistant
from inpui.exceptions import ServiceValidationError
import inpui.helpers.entity_registry as er

from tests.common import MockConfigEntry, snapshot_platform


@pytest.fixture
def platforms() -> list[Platform]:
    """Fixture to specify platforms to test."""
    return [Platform.NUMBER]


@pytest.mark.usefixtures("entity_registry_enabled_by_default", "init_integration")
async def test_number_entities(
    hass: HomeAssistant,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the number entities."""
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.usefixtures("entity_registry_enabled_by_default", "init_integration")
async def test_number_set_hysteresis_band(
    hass: HomeAssistant,
    mock_airobot_client: AsyncMock,
) -> None:
    """Test setting hysteresis band value."""
    await hass.services.async_call(
        NUMBER_DOMAIN,
        SERVICE_SET_VALUE,
        {
            ATTR_ENTITY_ID: "number.test_thermostat_hysteresis_band",
            ATTR_VALUE: 0.3,
        },
        blocking=True,
    )

    mock_airobot_client.set_hysteresis_band.assert_called_once_with(0.3)


@pytest.mark.usefixtures("entity_registry_enabled_by_default", "init_integration")
async def test_number_set_value_error(
    hass: HomeAssistant,
    mock_airobot_client: AsyncMock,
) -> None:
    """Test error handling when setting number value fails."""
    mock_airobot_client.set_hysteresis_band.side_effect = AirobotError("Device error")

    with pytest.raises(ServiceValidationError) as exc_info:
        await hass.services.async_call(
            NUMBER_DOMAIN,
            SERVICE_SET_VALUE,
            {
                ATTR_ENTITY_ID: "number.test_thermostat_hysteresis_band",
                ATTR_VALUE: 0.3,
            },
            blocking=True,
        )

    assert exc_info.value.translation_domain == "airobot"
    assert exc_info.value.translation_key == "set_value_failed"
