import secrets
from typing import Optional
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi_sso import SSOLoginError
from fastapi_sso.sso.discord import DiscordSSO
from pydantic import HttpUrl
from tortoise import timezone

from ...config import Settings
from ...models.db import Token as TokenDB, User as UserDB
from ...models.db.user import TokenType
from ...models.response.user import Token

settings=Settings()

discord_sso=DiscordSSO(client_id=settings.DISCORD_CLIENT_ID, # type: ignore
                       client_secret=settings.DISCORD_CLIENT_SECRET, # type: ignore
                       redirect_uri=settings.DISCORD_CLIENT_REDIRECT
                    )

router=APIRouter(tags=["Auth", "SSO", "Discord"], )

@router.get("/login", response_class=RedirectResponse)
async def discord_login(return_url:Optional[HttpUrl]=None):
    token=await TokenDB.create(token=secrets.token_hex(32), user=None,
                               expired_in=timezone.now()+settings.TOKEN_EXPIRE,
                               return_url=return_url, token_type=TokenType.oauth_state)
    print("token", token.token)
    async with discord_sso:
        return await discord_sso.get_login_redirect(state=token.token)

@router.get("/callback")
async def discord_callback(request: Request, state:str):
    state_token=await TokenDB.get_or_none(token=state, token_type=TokenType.oauth_state)
    if state_token is None:
        return PlainTextResponse("Error", status_code=401)
    if state_token.expired_in <= timezone.now():
        return PlainTextResponse("Error", status_code=401)
    
    async with discord_sso:
        try:
            user_info=await discord_sso.verify_and_process(request)
        except SSOLoginError:
            return PlainTextResponse("Error", status_code=401)
    if user_info is None:
        return PlainTextResponse("Error", status_code=401)
    
    user, _=await UserDB.get_or_create({
        "name": user_info.display_name,
        "password": ""
    }, mail=user_info.email)
    
    token=await TokenDB.create(token=secrets.token_hex(32), user=user, expired_in=timezone.now()+settings.TOKEN_EXPIRE)
    await state_token.delete()
    
    if "users" not in request.session:
        request.session["users"]=[]
    request.session["users"].append({"name":user.name, "id":str(user.id), "token":token.token, "expired_in":token.expired_in.isoformat()})
    
    if state_token.return_url is None:
        return Token(access_token=token.token, token_type="bearer", user_id=user.id, expired_in=token.expired_in)
    return RedirectResponse(state_token.return_url)