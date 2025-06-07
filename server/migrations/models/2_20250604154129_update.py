from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "token" ADD "token_type" VARCHAR(6) NOT NULL  DEFAULT 'bearer';
        ALTER TABLE "token" ADD "return_url" VARCHAR(512);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "token" DROP COLUMN "token_type";
        ALTER TABLE "token" DROP COLUMN "return_url";"""
