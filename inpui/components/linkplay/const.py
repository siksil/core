"""LinkPlay constants."""

from dataclasses import dataclass

from linkplay.controller import LinkPlayController

from inpui.const import Platform
from inpui.util.hass_dict import HassKey


@dataclass
class LinkPlaySharedData:
    """Shared data for LinkPlay."""

    controller: LinkPlayController
    entity_to_bridge: dict[str, str]


DOMAIN = "linkplay"
SHARED_DATA = "shared_data"
SHARED_DATA_KEY: HassKey[LinkPlaySharedData] = HassKey(SHARED_DATA)
PLATFORMS = [Platform.BUTTON, Platform.MEDIA_PLAYER, Platform.SELECT]
DATA_SESSION = "session"
