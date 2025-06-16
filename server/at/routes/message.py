from fastapi import APIRouter

from ..models.db import Thread

router=APIRouter(tags=["Message"])

@router.get("/")
async def get_threads():
    pass