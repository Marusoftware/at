from fastapi import APIRouter, Depends
from typing import List, Union
from uuid import UUID
from tortoise.expressions import Q

from ..exceptions import NotFound
from ..models.db import Thread as ThreadDB, User as UserDB
from ..models.response.message import Thread
from ..models.request.message import ThreadCreate
from .auth import get_user_no_error, get_user

router=APIRouter(tags=["Message"])

@router.get("/", response_model=List[Thread])
async def get_threads(user:Union[UserDB,None] = Depends(get_user_no_error)):
    if user is None:
        return await ThreadDB.filter(owner=None)
    if not user.is_verified:
        return await ThreadDB.filter(owner=None)
    return await ThreadDB.filter(Q(owner=None) | Q(owner=user))

@router.get("/{thread_id}/", response_model=Thread)
async def get_thread(thread_id:UUID, user:Union[UserDB,None] = Depends(get_user_no_error)):
    if user is None:
        thread=await ThreadDB.get_or_none(owner=None, id=thread_id)
    elif not user.is_verified:
        thread=await ThreadDB.get_or_none(owner=None, id=thread_id)
    else:
        thread=await ThreadDB.get_or_none(Q(owner=None) | Q(owner=user), id=thread_id)

    if thread is None:
        raise NotFound(detail="Thread not found")
    return thread

@router.post("/", response_model=Thread)
async def create_thread(thread:ThreadCreate, user:UserDB = Depends(get_user)):
    thread_db = await ThreadDB.create(**thread.model_dump(), owner=user)
    return thread_db