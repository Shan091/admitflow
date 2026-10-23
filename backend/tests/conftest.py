"""Tests use explicit configuration and never implicitly load developer credentials."""

import os

from src.core.settings import Settings, get_settings

# Apply before test collection imports the application/broker. Environment variables
# and explicit Settings(_env_file=...) fixtures continue to work. Runtime CLI settings
# are unchanged, and the developer's .env stays in place while the gate runs.
Settings.model_config["env_file"] = None
os.environ["PYTHON_DOTENV_DISABLED"] = "1"
get_settings.cache_clear()
