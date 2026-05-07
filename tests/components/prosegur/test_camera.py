"""The camera tests for the prosegur platform."""

import logging
from unittest.mock import AsyncMock

from pyprosegur.exceptions import ProsegurException
import pytest

from inpui.components import camera
from inpui.components.camera import Image
from inpui.components.prosegur.const import DOMAIN
from inpui.const import ATTR_ENTITY_ID
from inpui.core import HomeAssistant
from inpui.exceptions import HomeAssistantError


async def test_camera(hass: HomeAssistant, init_integration) -> None:
    """Test prosegur get_image."""

    image = await camera.async_get_image(hass, "camera.contract_1234abcd_test_cam")

    assert image == Image(content_type="image/jpeg", content=b"ABC")


async def test_camera_fail(
    hass: HomeAssistant,
    init_integration,
    mock_install,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test prosegur get_image fails."""

    mock_install.get_image = AsyncMock(
        return_value=b"ABC", side_effect=ProsegurException()
    )

    with (
        caplog.at_level(logging.ERROR, logger="inpui.components.prosegur"),
        pytest.raises(HomeAssistantError) as exc,
    ):
        await camera.async_get_image(hass, "camera.contract_1234abcd_test_cam")

    assert "Unable to get image" in str(exc.value)

    assert "Image test_cam doesn't exist" in caplog.text


async def test_request_image(
    hass: HomeAssistant, init_integration, mock_install
) -> None:
    """Test the camera request image service."""

    await hass.services.async_call(
        DOMAIN,
        "request_image",
        {ATTR_ENTITY_ID: "camera.contract_1234abcd_test_cam"},
    )
    await hass.async_block_till_done()

    assert mock_install.request_image.called


async def test_request_image_fail(
    hass: HomeAssistant,
    init_integration,
    mock_install,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test the camera request image service fails."""

    mock_install.request_image = AsyncMock(side_effect=ProsegurException())

    with caplog.at_level(logging.ERROR, logger="inpui.components.prosegur"):
        await hass.services.async_call(
            DOMAIN,
            "request_image",
            {ATTR_ENTITY_ID: "camera.contract_1234abcd_test_cam"},
        )
        await hass.async_block_till_done()

        assert mock_install.request_image.called

        assert "Could not request image from camera test_cam" in caplog.text
