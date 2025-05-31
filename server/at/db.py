from .models import db as db_models
from .config import Settings

settings=Settings()

DB_CONFIG={
    "connections": {"default":settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": [db_models, "aerich.models"],
            "default_connection": "default",
        },
    },
}