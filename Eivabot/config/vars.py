# Configs imports from here

"""Select the runtime configuration without requiring a private config file."""
import os

if os.environ.get("ENV", "").strip().lower() in {"1", "true", "yes", "on"}:
    from Eiva_config import Config
elif os.path.isfile("config.py"):
    from config import Development as Config
else:
    from .Config import Config

# Eivabot
