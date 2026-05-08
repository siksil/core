"""Constants for the Inpui Cloud integration."""

DOMAIN = "inpui_cloud"

# API Endpoints (Update with production URL later)
ATTR_API_BASE_URL = "https://api.inpuismart.com/v1"
ATTR_HARDWARE_PAIR_URL = f"{ATTR_API_BASE_URL}/hardware/pair"
ATTR_HARDWARE_HEARTBEAT_URL = f"{ATTR_API_BASE_URL}/hardware/heartbeat"
ATTR_ICE_SERVERS_URL = f"{ATTR_API_BASE_URL}/hardware/ice-servers"

# Configuration keys
CONF_PAIRING_CODE = "pairing_code"
CONF_HUB_ID = "hub_id"
CONF_JWT_TOKEN = "jwt_token"
CONF_TUNNEL_TOKEN = "tunnel_token"
CONF_REMOTE_URL = "remote_url"

# Entity IDs
BINARY_SENSOR_CONNECTED = "binary_sensor.inpui_cloud_connected"
