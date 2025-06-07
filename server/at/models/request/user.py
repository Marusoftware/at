from typing import Optional
from pydantic import BaseModel, EmailStr

class UserUpdate(BaseModel):
    name:Optional[str]=None
    mail:Optional[EmailStr]=None
    oldPassword:Optional[str]=None
    newPassword:Optional[str]=None