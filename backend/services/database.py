"""
Database connection module for MongoDB (Atlas-friendly).
Fetches the newest mega-document from the collection.
"""

import os
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi

from pymongo.errors import (
    ServerSelectionTimeoutError,
    ConfigurationError,
    OperationFailure,
)

# Load environment variables from backend/.env (safe if already loaded elsewhere)
backend_dir = Path(__file__).parent.parent
env_path = backend_dir / ".env"
load_dotenv(dotenv_path=str(env_path), override=False)

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("MONGODB_DB_NAME", "admit_tree_db")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION", "programs")

_client: MongoClient | None = None
_database = None


def get_database():
    """
    Creates and returns a cached MongoDB database instance.
    Raises helpful errors if Atlas connection/auth/network is wrong.
    """
    global _client, _database

    if _database is not None:
        return _database

    if not MONGODB_URI:
        raise ValueError(
            "MONGODB_URI environment variable is not set. "
            "Add it to backend/.env"
        )

    try:
        _client = MongoClient(
            MONGODB_URI,
            tls=True,
            tlsCAFile=certifi.where(),
            connectTimeoutMS=10000,
            serverSelectionTimeoutMS=10000,
        )

        # Fail fast if unreachable / DNS / IP not allowed / auth wrong
        _client.admin.command("ping")

        _database = _client[DATABASE_NAME]
        return _database

    except ConfigurationError as e:
        raise RuntimeError(
            f"MongoDB configuration error: {e}. "
            "Check your connection string format (mongodb+srv://...)"
        ) from e

    except OperationFailure as e:
        # Auth failures, not authorized, etc.
        raise RuntimeError(
            f"MongoDB auth/operation failure: {e}. "
            "Check username/password and DB permissions in Atlas."
        ) from e

    except ServerSelectionTimeoutError as e:
        # Most common: IP not whitelisted or DNS/network issue
        raise RuntimeError(
            f"MongoDB connection timeout: {e}. "
            "Common causes: Atlas Network Access IP not allowed, "
            "wrong cluster hostname, or network/DNS issues."
        ) from e


def get_universities_collection():
    """
    Returns the configured collection that stores the mega document.
    """
    db = get_database()
    return db[COLLECTION_NAME]


def fetch_university_data():
    """
    Fetch the newest mega-document from MongoDB.
    Expected doc shape:
      {
        _id: ...,
        apply_deadline: "...",
        "University of Toronto": { ec_quality, "co-op", programs: {...}},
        ...
      }
    """
    collection = get_universities_collection()

    doc = collection.find_one(sort=[("_id", -1)])
    if not doc:
        raise ValueError(
            f"No documents found in MongoDB collection '{COLLECTION_NAME}' "
            f"in database '{DATABASE_NAME}'."
        )

    return doc


def close_connection():
    """
    Close MongoDB connection.
    """
    global _client, _database
    if _client is not None:
        _client.close()
    _client = None
    _database = None
