from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(1024) NOT NULL UNIQUE,
    "password" VARCHAR(1024) NOT NULL,
    "mail" VARCHAR(1024) NOT NULL UNIQUE,
    "created_in" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_verified" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "thread" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(512) NOT NULL,
    "created_in" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "owner_id" UUID REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "message" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "text" TEXT NOT NULL,
    "created_in" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "last_update" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "thread_id" UUID NOT NULL REFERENCES "thread" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "token" (
    "token" VARCHAR(1024) NOT NULL  PRIMARY KEY,
    "created_in" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "expired_in" TIMESTAMPTZ NOT NULL,
    "token_type" VARCHAR(6) NOT NULL  DEFAULT 'bearer',
    "return_url" VARCHAR(512),
    "user_id" UUID REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "token"."token_type" IS 'bearer: bearer\noauth_state: state\nmail_verify: mail';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
