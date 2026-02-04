from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(1024) NOT NULL UNIQUE,
    "display_name" VARCHAR(1024) NOT NULL,
    "password" VARCHAR(1024),
    "mail" VARCHAR(1024) NOT NULL UNIQUE,
    "created_in" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_verified" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "connection" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "connection_type" VARCHAR(7) NOT NULL,
    "connection_id" VARCHAR(1024) NOT NULL,
    "openid" JSONB NOT NULL,
    "user_id" UUID REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_connection_connect_1f8cb8" ON "connection" ("connection_id");
COMMENT ON COLUMN "connection"."connection_type" IS 'discord: discord';
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
    "token_type" VARCHAR(20) NOT NULL  DEFAULT 'bearer',
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


MODELS_STATE = (
    "eJztm1tP4zgUgP9KlKcZiUXQKTBCq5HaUna6A+0KyuxoLorcxG0tEieTOAsV4r+v7cS5OG"
    "4npYUmTF4oPT4nsT9fzqXJg+64FrSD/Z6LMTQJcrF+qj3oGDiQ/qNo3dN04HlpGxMQMLG5"
    "upnXmwTEByahLVNgB5CKLBiYPvLi++DQtpnQNakiwrNUFGL0M4QGcWeQzKFPG779oGKELX"
    "gPA/HVuzWmCNpWrsvIYvfmcoMsPC67uRmcnXNNdruJYbp26OBU21uQuYsT9TBE1j6zYW0z"
    "iKEPCLQyw2C9jMcsRFGPqYD4IUy6aqUCC05BaDMY+p/TEHNKGr8T+9P+oK+Bh3JmaBEmjM"
    "XDYzSqdMxcqrNb9T52rt68O37LR+kGZObzRk5Ef+SGgIDIlHNNQaaTGYEpUO3Ngd/HocPJ"
    "DmiPADZhgbDiMhJuOpSngBaClHS6ygRqgTDHVbdQYLq+darF/+ilKOsOuDdsiGdkTr+erI"
    "D+uXPFuZ+85YiVSFXLlAFVL9OC4XMhLCxWJcHSKzPP7PCg1S6BjanJ5FwPYhWyv69HQzWy"
    "1EJidYPpIL5ZyCR7mo0C8uNFF982NjUbNOu0EwQ/bSYYCnSXnS98q7v03I2O5GHvYtSVdz"
    "+7QFciHAbQV67K5YdnxmSDEzRectVA+4vzknmd6a3yuGQwivDOXR+iGf4EF4VTUkIWu9qb"
    "+DJVhZZK01744C5xxNlFQUdHxwRJdLh1rnuds77OGU6AeXsHfMvIwWQtbsuVJIlusclpOb"
    "IEYDDj42ejYH2OuV7CIKAtquhGNK0MbZyMUhPX1DmuIfCeFFGOqVSNUujvOGrZBrVx/8t4"
    "teNwFnHLxWj4l1CXvYkU1PiQjd9AuEj1jLYQ5MAlUU3OUuJrxab74p9q0tbpGKwRthfxjl"
    "hFf3DZvx53Lv/JTcFZZ9xnLa0cfiF9cyz58+Qi2r+D8UeNfdW+joZ9eSMkeuOvOusTCIlr"
    "YPfOAFZm8wqpAJObWBsExAg9xn/dmZVMm6nd6dTGnc8cgXM2tDWjvZzRNj1LlQO+SkTItS"
    "JWmRB5d9Q2j5GLm3UL3MbJhepLLncIVSm/iOEq0osU+/LsIp3jJrmodXLBPwsolxf2hH5d"
    "kot8Qe/osFWinke1CoXQJmd4DYFlMWdw7/DaQVLWpqkjchpNITG/LNb19BknHNXtgiLRbm"
    "x5/ukK2kD8aKmGmSkRVu84WQb08VnjHfcWKn8rjhpWRzuJyk6CneT2ZZ10YrAdL/3rYGen"
    "P7qt+EW48dqv02vDew/5T5rYvGU9J7YmEymGvXIm+VG10fMa+Su8XF6iTyDwo5BFelwjaj"
    "jVos/v2KUE5gbtPoGnGv/4jh2AbOM/6KPp4lRjX/QnHJWtgxIHZetATmZ8SEIfG6Fvr+NU"
    "8lZP4vzysduW0r/mWQO9RoXU6qYIFX3WgHNVhMaC9/LIWExsUwVsqoCvNb9IMVko8GywMN"
    "bFJdvVs3i6ATgPBMFd/OBqWWhZm1pGGxvwEgFhWVZC/zfbj01+/0rzexREuRGCiiOj67o2"
    "BHiJk89bSjM7oabPNZnrxj3lHXt3NLrITVx3ID/mdnPZ7dM9wmeMKqEorBwMx6q4vEwZOn"
    "2Af8NKdP5VnMod2Utr0bnj+DeuyRef7NgQQ+mnOiq6GHi9aVMGokBfHwTPmX926IltznVF"
    "Bhq37K3KQUGqU5ksdICXPJytTEIZZmkxxDO/0zCNv33wR+uwfdJ+/+64/Z6q8J4kklXvlE"
    "W+Z29F0kn9dBDvkrJxbsaknjlU6+ioTMn26EgOddnyXwNUrF5PSIcHZeraVEvxuiKBWPGy"
    "xPK37jImzWt3ciQvXrtbI4Lcvpt4/B9pUB2U"
)
