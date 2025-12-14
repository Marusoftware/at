from enum import StrEnum
from tortoise import Model
from tortoise.fields import *

class User(Model):
    id=UUIDField(pk=True)
    name=CharField(1024, unique=True)
    password=CharField(1024, null=True)
    mail=CharField(1024, unique=True)
    created_in=DatetimeField(auto_now_add=True)
    is_verified=BooleanField(default=False)
    tokens:ReverseRelation["Token"]
    connections: ReverseRelation["Connection"]

class TokenType(StrEnum):
    bearer="bearer"
    oauth_state="state"
    mail_verify="mail"

class Token(Model):
    token=CharField(1024, pk=True)
    created_in=DatetimeField(auto_now_add=True)
    expired_in=DatetimeField()
    token_type=CharEnumField(TokenType, default=TokenType.bearer, max_length=20)
    return_url=CharField(max_length=512, null=True)
    user:ForeignKeyNullableRelation[User]=ForeignKeyField("models.User", related_name="tokens", null=True)

class ConnectionType(StrEnum):
    discord="discord"

class Connection(Model):
    id=UUIDField(pk=True)
    connection_type=CharEnumField(ConnectionType)
    connection_id=CharField(max_length=1024, index=True)
    openid =JSONField()
    user:ForeignKeyNullableRelation[User]=ForeignKeyField("models.User", related_name="connections", null=True)

from .message import Message, Thread
