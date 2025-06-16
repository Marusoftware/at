from tortoise import Model
from tortoise.fields import *

class Thread(Model):
    id=UUIDField(pk=True)
    name=CharField(512)
    created_in=DatetimeField(auto_now_add=True)
    owner:ForeignKeyNullableRelation["User"]=ForeignKeyField("models.User", related_name="threads", null=True)
    messages:ReverseRelation["Message"]

class Message(Model):
    id=UUIDField(pk=True)
    text=TextField()
    created_in=DatetimeField(auto_now_add=True)
    last_update=DatetimeField(auto_now=True)
    user:ForeignKeyRelation["User"]=ForeignKeyField("models.User", related_name="messages")
    thread:ForeignKeyRelation[Thread]=ForeignKeyField("models.Thread", related_name="messages")

from .user import User