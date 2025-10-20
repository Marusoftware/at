from fastapi import APIRouter, Depends
from typing import List, Union
from uuid import UUID
from tortoise.expressions import Q
from tortoise.query_utils import Prefetch

from ..exceptions import APIError, NotFound
from ..models.db import Thread as ThreadDB, User as UserDB, Message as MessageDB
from ..models.response.message import Thread, Message, ThreadWithMessages
from ..models.request.message import ThreadCreate, ThreadUpdate, MessageCreate, MessageUpdate
from .auth import get_user_no_error, get_user

router=APIRouter(tags=["Message"])

MESSAGE_GET_LIMIT=100

@router.get("/", response_model=List[Thread])
async def get_threads(user:Union[UserDB,None] = Depends(get_user_no_error)):
    if user is None:
        return await ThreadDB.filter(owner=None)
    if not user.is_verified:
        return await ThreadDB.filter(owner=None)
    return await ThreadDB.filter(Q(owner=None) | Q(owner=user))

@router.get("/{thread_id}/", response_model=ThreadWithMessages)
async def get_thread(thread_id:UUID, user:Union[UserDB,None] = Depends(get_user_no_error), offset:int=0, limit:int=MESSAGE_GET_LIMIT):
    if MESSAGE_GET_LIMIT < limit:
        raise APIError(detail="limit out of range")
    if user is None:
        thread=await ThreadDB.get_or_none(owner=None, id=thread_id).prefetch_related(Prefetch("messages", MessageDB.all().order_by("-created_in").offset(offset).limit(limit)))
    elif not user.is_verified:
        thread=await ThreadDB.get_or_none(owner=None, id=thread_id).prefetch_related(Prefetch("messages", MessageDB.all().order_by("-created_in").offset(offset).limit(limit)))
    else:
        thread=await ThreadDB.get_or_none(Q(owner=None) | Q(owner=user), id=thread_id).prefetch_related(Prefetch("messages", MessageDB.all().order_by("-created_in").offset(offset).limit(limit)))
    if thread is None:
        raise NotFound(detail="Thread not found")
    return thread

@router.post("/", response_model=Thread)
async def create_thread(thread:ThreadCreate, user:UserDB = Depends(get_user)):
    thread_db = await ThreadDB.create(**thread.model_dump(), owner=user)
    return thread_db

@router.put("/{thread_id}/", response_model=Thread)
async def update_thread(thread_id:UUID, thread_update:ThreadUpdate, user:UserDB = Depends(get_user)):
    thread=await ThreadDB.get_or_none(owner=user, id=thread_id)
    if thread is None:
        raise NotFound(detail="Thread not found")
    thread.update_from_dict(thread_update.model_dump(exclude_unset=True))
    await thread.save()
    return thread

@router.delete("/{thread_id}/", response_model=Thread)
async def delete_thread(thread_id:UUID, user:UserDB = Depends(get_user)):
    thread=await ThreadDB.get_or_none(owner=user, id=thread_id)
    if thread is None:
        raise NotFound(detail="Thread not found")
    await thread.delete()
    return thread

@router.post("/{thread_id}/", response_model=Message)
async def create_message(thread_id:UUID, message:MessageCreate, user:UserDB = Depends(get_user)):
    thread=await ThreadDB.get_or_none(owner=user, id=thread_id)
    if thread is None:
        raise NotFound(detail="Thread not found")
    message_db = await MessageDB.create(**message.model_dump(), user=user, thread=thread)
    return message_db

@router.put("/{thread_id}/{message_id}/", response_model=Message)
async def update_message(thread_id:UUID, message_id:UUID, message_update:MessageUpdate, user:UserDB = Depends(get_user)):
    message=await MessageDB.get_or_none(id=message_id, user=user)
    if message is None:
        raise NotFound(detail="Message not found")
    message.update_from_dict(message_update.model_dump(exclude_unset=True))
    await message.save()
    return message

@router.delete("/{thread_id}/{message_id}/", response_model=Message)
async def delete_message(thread_id:UUID, message_id:UUID, user:UserDB = Depends(get_user)):
    message=await MessageDB.get_or_none(id=message_id, user=user)
    if message is None:
        raise NotFound(detail="Message not found")
    await message.delete()
    return message