"""Optional MongoDB handle. Connection checks are explicit and bounded."""
import logging
import os

from pymongo import MongoClient
from pymongo.errors import ConfigurationError, PyMongoError

logger = logging.getLogger(__name__)
MONGO_DB_URL = os.environ.get("MONGO_DB_URL") or os.environ.get("MONGO_URI")
client = None
db = None
if MONGO_DB_URL:
    try:
        client = MongoClient(MONGO_DB_URL, serverSelectionTimeoutMS=5000)
        db = client["Eiva"]["datas"]
    except (ConfigurationError, PyMongoError, ValueError):
        logger.exception("MongoDB configuration failed")


def validate_connection():
    """Raise a useful error if MongoDB is requested but unavailable."""
    if client is None:
        raise RuntimeError("Set MONGO_DB_URL to enable MongoDB features")
    client.admin.command("ping")
    return True
