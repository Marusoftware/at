from typing import Optional, List
from pydantic import HttpUrl, computed_field
from functools import cached_property
from pydantic_settings import BaseSettings
import secrets
from datetime import timedelta as _timedelta

class Settings(BaseSettings):
    DATABASE_URL:str ="sqlite://./test.db"
    MAIL_CALLBACK_URL:str = "http://localhost:8000/auth/mail_verify"
    SECRET:str = secrets.token_urlsafe(15)
    SERVE_STATIC:Optional[str] = None
    TZ:str = "Asia/Tokyo"
    TOKEN_EXPIRE:_timedelta = _timedelta(hours=1)
    DEFAULT_RETURN_URL:HttpUrl=HttpUrl("https://marusoftware.net")
    ORIGIN_URL:HttpUrl = HttpUrl("http://localhost:8000")
    AUTH_ALLOWED_ORIGINS: List[HttpUrl] = []
    DISCORD_CLIENT_ID: Optional[str]=None
    DISCORD_CLIENT_SECRET: Optional[str]=None
    DISCORD_CLIENT_REDIRECT: str="http://localhost:8000/auth/sso/discord/callback"
    MAIL_SERVER:Optional[str]=None
    MAIL_VERIFY_SUBJECT:str = "Marusoftware: Email Verification"
    MAIL_VERIFY_FROM:str = "noreply@marusoftware.net"
    MAIL_OPTIONS:dict={}
    SERVICE_NAME:str="@Marusoftware"
    MTA_MODE:bool=False
    
    @computed_field
    @cached_property
    def AUTH_ALLOWED_HOSTS(self) -> List[str]:
        return [(origin.host if origin.port is None else f"{origin.host}:{origin.port}") for origin in self.AUTH_ALLOWED_ORIGINS if origin.host is not None]

    class Config:
        env_file = ".env"