"""TinyDB controlling functions."""

from logging import getLogger

from tinydb import Query, TinyDB

from src.app.schemas.example_schemas import Example

logger = getLogger(__name__)


# Initialize the TinyDB database
db = TinyDB("/src/db.json")
logs = db.table("logs")


def insert_entries(logs) -> bool:
    """Insert multiple entries in TinyDB"""
    try:
        logs.insert_multiple(logs)
    except Exception as e:
        logger.error("Failed to insert new logs in DB: %s", e)
        return False
    return True


# def search_by_kid(kid: str) -> None:
#     """Search for keys by a list of IDs."""
#     key_q = Query()
#     return logs.search(key_q.keys.any(lambda key: key["kid"] == kid))


# def add_keys(keys: None):
#     """Add a set of keys and their id."""
#     key = Query()
#     existing_key = logs.get(key.id == keys.id)
#     if existing_key:
#         logs.update(keys.model_dump(), key.id == keys.id)
#     else:
#         logs.insert({"id": keys.id, **keys.model_dump()})


# def delete_by_id(_id: str):
#     """Delete a set of keys by id."""
#     key = Query()
#     logs.remove(key.id == _id)
