"""Minimal Superset config for the dhis2-docker dev stack.

Mounted into every superset container via compose.superset.yml at
/app/pythonpath/superset_config.py so all services share one metadata DB.
"""

import os

SECRET_KEY = os.environ.get(
    "SUPERSET_SECRET_KEY",
    "dev-secret-key-change-me-for-anything-real",
)

SQLALCHEMY_DATABASE_URI = os.environ.get(
    "SQLALCHEMY_DATABASE_URI",
    "postgresql+psycopg2://superset:superset@superset-db:5432/superset",
)

REDIS_HOST = os.environ.get("REDIS_HOST", "superset-redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": 1,
}
DATA_CACHE_CONFIG = CACHE_CONFIG
FILTER_STATE_CACHE_CONFIG = CACHE_CONFIG
EXPLORE_FORM_DATA_CACHE_CONFIG = CACHE_CONFIG

SQLLAB_CTAS_NO_LIMIT = True
