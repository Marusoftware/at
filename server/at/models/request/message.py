from uuid import UUID
from pydantic import BaseModel
from typing import Optional

class ThreadCreate(BaseModel):
    name: str

class ThreadUpdate(BaseModel):
    name: Optional[str] = None

class MessageCreate(BaseModel):
    text: str

class MessageUpdate(BaseModel):
    text: Optional[str] = None