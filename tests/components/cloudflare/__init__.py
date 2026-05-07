"""Tests for the Cloudflare integration."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, Mock, patch

import pycfdns

from inpui.components.cloudflare.const import CONF_RECORDS, DOMAIN
from inpui.const import CONF_API_TOKEN, CONF_ZONE
from inpui.core import HomeAssistant
from inpui.helpers.typing import UNDEFINED, UndefinedType

from tests.common import MockConfigEntry

ENTRY_CONFIG = {
    CONF_API_TOKEN: "mock-api-token",
    CONF_ZONE: "mock.com",
    CONF_RECORDS: ["ha.mock.com", "inpui.mock.com"],
}

ENTRY_OPTIONS = {}

USER_INPUT = {
    CONF_API_TOKEN: "mock-api-token",
}

USER_INPUT_ZONE = {CONF_ZONE: "mock.com"}

USER_INPUT_RECORDS = {CONF_RECORDS: ["ha.mock.com", "inpui.mock.com"]}

MOCK_ZONE: pycfdns.ZoneModel = {"name": "mock.com", "id": "mock-zone-id"}
MOCK_ZONE_RECORDS: list[pycfdns.RecordModel] = [
    {
        "id": "zone-record-id",
        "type": "A",
        "name": "ha.mock.com",
        "proxied": True,
        "content": "127.0.0.1",
    },
    {
        "id": "zone-record-id-2",
        "type": "A",
        "name": "inpui.mock.com",
        "proxied": True,
        "content": "127.0.0.1",
    },
    {
        "id": "zone-record-id-3",
        "type": "A",
        "name": "mock.com",
        "proxied": True,
        "content": "127.0.0.1",
    },
]


async def init_integration(
    hass: HomeAssistant,
    *,
    data: dict[str, Any] | UndefinedType = UNDEFINED,
    options: dict[str, Any] | UndefinedType = UNDEFINED,
    unique_id: str = MOCK_ZONE["name"],
    skip_setup: bool = False,
) -> MockConfigEntry:
    """Set up the Cloudflare integration in Home Assistant."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=ENTRY_CONFIG if data is UNDEFINED else data,
        options=ENTRY_OPTIONS if options is UNDEFINED else options,
        unique_id=unique_id,
    )
    entry.add_to_hass(hass)

    if not skip_setup:
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    return entry


def get_mock_client() -> Mock:
    """Return of Mock of pycfdns.Client."""
    client = Mock()

    client.list_zones = AsyncMock(return_value=[MOCK_ZONE])
    client.list_dns_records = AsyncMock(return_value=MOCK_ZONE_RECORDS)
    client.update_dns_record = AsyncMock(return_value=None)

    return client


def patch_async_setup_entry() -> AsyncMock:
    """Patch the async_setup_entry method and return a mock."""
    return patch(
        "inpui.components.cloudflare.async_setup_entry",
        return_value=True,
    )
