from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class Thread(BaseModel):
    id: UUID
    name: str
    created_in: datetime
    owner_id: UUID

class Message(BaseModel):
    id: UUID
    text: str
    created_in: datetime
    last_update: datetime
    user_id: UUID
    thread_id: UUID