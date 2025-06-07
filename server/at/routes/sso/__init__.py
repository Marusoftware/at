from fastapi import APIRouter
from ...config import Settings

router = APIRouter(tags=["Auth","SSO"])
settings=Settings()

if settings.DISCORD_CLIENT_ID and settings.DISCORD_CLIENT_SECRET:
    from .discord import router as discord_router
    router.include_router(discord_router, prefix="/discord")