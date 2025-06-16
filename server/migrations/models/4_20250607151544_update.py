from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
    CREATE TABLE IF NOT EXISTS "thread" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(512) NOT NULL,
    "created_in" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS "message" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "text" TEXT NOT NULL,
    "created_in" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "last_update" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "thread_id" UUID NOT NULL REFERENCES "thread" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
    );
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "message";
        DROP TABLE IF EXISTS "thread";"""
