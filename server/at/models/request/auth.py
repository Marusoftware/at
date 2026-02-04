from pydantic import BaseModel, EmailStr, SecretStr, Field
from typing import Optional

class UserCreate(BaseModel):
    mail:EmailStr

class UserAuthUpdate(BaseModel):
    name:str=Field(max_length=1024)
    password:SecretStr

class AuthCallbackData(BaseModel):
    mail_token:Optional[str]=None