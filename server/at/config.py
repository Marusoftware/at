from typing import Optional
from pydantic import HttpUrl
from pydantic_settings import BaseSettings
import secrets
from datetime import timedelta as _timedelta

class Settings(BaseSettings):
    DATABASE_URL:str ="sqlite://./test.db"
    CALLBACK_URL:str = "http://localhost:8000/auth/callback"
    SECRET:str = secrets.token_urlsafe(15)
    SERVE_STATIC:Optional[str] = None
    TZ:str = "Asia/Tokyo"
    TOKEN_EXPIRE:_timedelta = _timedelta(hours=1)
    DEFAULT_RETURN_URL:HttpUrl=HttpUrl("https://marusoftware.net")
    DISCORD_CLIENT_ID: Optional[str]=None
    DISCORD_CLIENT_SECRET: Optional[str]=None
    DISCORD_CLIENT_REDIRECT: str="http://localhost:8000/auth/sso/discord/callback"
    MAIL_SERVER:Optional[str]=None
    MAIL_OPTIONS:dict={}
    MTA_MODE:bool=False

    class Config:
        env_file = ".env"