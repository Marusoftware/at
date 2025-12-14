from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(1024) NOT NULL UNIQUE,
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
COMMENT ON COLUMN "token"."token_type" IS 'bearer: bearer
oauth_state: state
mail_verify: mail';
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
    "eJztWm1vozgQ/iuIT7vSXtVm0+0qOp2UpOltbpvk1JK71e5WyAE3QQWbBXNpVPW/n20wGP"
    "JGCERJmi9NGeyZ8TP2vHh4UR1sQts/G/rQUxvKiwpcl/5GZPWDoiLgwIQSDqRkAkY2pwcR"
    "wUImfIY+Jf14oI9g5BMPGIQ+PwLbh5TkPumPFrRNLkewtUw2OUDWr4A9Ey9gQ034CAKbTV"
    "Z/fwyQQSyMlCCwzDP2p/5HItBMJqHAtiOthEhzpBvYDhyUiDKxQTWz0JiS2AxKGkMEPUA4"
    "LzGTa6qTmcu1HA671zdcd/rKwIitzUKErfbllevrG57lMjUTtu6MTDCKeXD1GSM1VCyRwN"
    "mobEz7S/Pu3cdP79kQF/tk7PGXXL76+rpY/ccI1xh7p+ZkKLiGMxQTECCREoPw35UmicRu"
    "jL/gXMgC7QnwlllAdcCzbkM0JhP6eHFeq+e1CeWywhr/NO+4QRjH9xz+BCYX+P4Ue+ndGy"
    "97OVZiiASWAFjGSmZ/FHg5wLKr2VaC81HAZHiQ6atbqOjGAgHBOsLTxXttIYJpoYVwvKZv"
    "ieXApVhSEeYA2bPIrnmRNCO+Z+IfVVqiDkxpnyxBW+v2Ovdas/c3m+n4/i+b69vUOuxNjV"
    "NnGeq70ANjGsDCIBczUf7tal8U9qh8H/Q7WT8dj9O+Zwxr+fp/0LOohutchqCs9BmLA1xa"
    "RiFDtjC2IUDbBrsRZbPiCLQGg9uUPVpdLY14f9hrdegZ4YaggyzCyd2+RoF9WKZFCKtO8B"
    "iSCc9oeLAbAeNpCjxTT4VK6dRhhCBPMvwS/Xkh+CNNb77eQRvwxRU3QpSytePVqWLHCHbJ"
    "aZQ8NfR9MIZlIBHP2hcoeuHacuFAJsxnHeOG0PjK8oGAn+BRHgqNLWwpBCmnkUmemaAUkz"
    "xlUywurpuIoBQsnOL55WdUMesDTqnWFkoJkqKC3ekOp0ujGwOGUa3dvG83r3k24YFpbGyu"
    "mR6WrWmMb7AHrTH6Cmcc6S4FGSADbn8sRHm/9FRsVVuestsjzW7hs2t5uzZsWmglhi3TkN"
    "Ia9tiS3PeH61ptSXUEgSdf/W1SqaSlFA4zHRQ46xxgOuTUzudNGq2koYS/PxGmlpvolCOB"
    "DYX//ETsliGsrmYNRVw5FIpRtfNs0e9BEnhIDzy7xDAkw50WUHFUv7yolRvUKcMsYlJgrA"
    "Auifsh3xaXUyXnTIWb9GgYEzVPLhwNlZNhEJMqaiMUTYVz7YKIV3oTdBFZel7GbMRvtYv6"
    "Vf3zx0/1z3QIVyGmXOXdJiw7W75BwtuSHMnw1pkd9Yx+VJeVdWcgm0FiX7H3ql1eluu9KM"
    "Os92IHpCKgItaVF24Lwuh2ddtcUKQKEBju7iqAktgXAuuv+0F/Wx8/RPTtD9MyyAfFtnzy"
    "sAIpJi+VGfYFdr3mt0wW2G/fDlrZoMAYtHYdFaKbplw3JPGlVHJFEpNOzeW9aC4nyOIp2t"
    "dLE67aMd2azHXkS3SDO+rJ76ImOF0uHenlknygK6j2ZPaH7L/Lboq+5T5gzvRGsMmT30gi"
    "4wTHSWinDGfPMpySukIbbv1DbAvNN833FLdQud0it6bXvnVySOBzZTWy4F3ozGt08rZnfn"
    "UuqHW+aatL4jg7uR30/xTDs3XyKYt8E1mkDXyiBy5bRgmWzRkzM0JPlq2kZSm79Ur8oCzg"
    "sBOgKlpoCzE79dA2vy2VPtTMU1Gkv+uMiwojRT7VFcdZV5y+NlPXfm0WH4Q837Ns00nKit"
    "nhBy0LOsWqafkG9syGEv2jbppZizz6akFTTqx189CR0x/MyTjgr1ClS0wXouqibcL9bTUz"
    "T98E7V8+8/o/llOW8Q=="
)
