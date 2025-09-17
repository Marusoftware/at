from pydantic import BaseModel

class ThreadCreate(BaseModel):
    name: str