from enum import StrEnum
from tortoise import Model
from tortoise.fields import *

class User(Model):
    id=UUIDField(pk=True)
    name=CharField(1024, unique=True)
    password=CharField(1024)
    mail=CharField(1024, unique=True)
    created_in=DatetimeField(auto_now_add=True)
    tokens:ReverseRelation["Token"]

class TokenType(StrEnum):
    bearer="bearer"
    oauth_state="state"

class Token(Model):
    token=CharField(1024, pk=True)
    created_in=DatetimeField(auto_now_add=True)
    expired_in=DatetimeField()
    token_type=CharEnumField(TokenType, default=TokenType.bearer)
    return_url=CharField(max_length=512, null=True)
    user:ForeignKeyNullableRelation[User]=ForeignKeyField("models.User", related_name="tokens", null=True)