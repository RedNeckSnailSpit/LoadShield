import os

VERSION = "0.0.1"
APP_STATE = "development"  # Options: development, staging, alpha, beta, release
CONFIG_DIR = "configs"
CONFIG_FILE_NAME = "config.json"
LOADSHEDDING_FILE_NAME = "loadshedding.json"
CONFIG_FILE_LOCATION = os.path.join(CONFIG_DIR, CONFIG_FILE_NAME)
LOADSHEDDING_FILE_LOCATION = os.path.join(CONFIG_DIR, LOADSHEDDING_FILE_NAME)

THESPEAR_API_BASE_URL = "https://loadshedding.apis.thespear.dev"
THESPEAR_API_VERSION = "v1"
ESP_API_BASE_URL = "https://api.eskomsepush.com"
UPDATE_INFO_URL = "https://placeholder.updateinfo.url"

def get_version():
    version_map = {
        "development": f"{VERSION}d",
        "staging": f"{VERSION}s",
        "alpha": f"{VERSION}a",
        "beta": f"{VERSION}b",
        "release": VERSION,
    }
    return version_map.get(APP_STATE, VERSION)

def ensure_directories():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        open(CONFIG_FILE_LOCATION, 'w').close()
        open(LOADSHEDDING_FILE_LOCATION, 'w').close()
