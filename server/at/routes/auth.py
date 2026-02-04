from email.message import EmailMessage
from typing import List, Optional, Union
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, Depends, Request
import secrets
from passlib.context import CryptContext
from pydantic import HttpUrl
from tortoise.expressions import Q
from tortoise import timezone

from ..mail import mail
from ..exceptions import APIError, Forbidden
from ..models.response.user import User, Token
from ..models.request.auth import UserCreate, AuthCallbackData
from ..models.db.user import TokenType
from ..models.db import User as UserDB, Token as TokenDB
from ..config import Settings

router=APIRouter(tags=["Auth"], include_in_schema=False)
oauth=OAuth2PasswordBearer(tokenUrl="/auth/signin")
oauth_no_error=OAuth2PasswordBearer(tokenUrl="/auth/signin", auto_error=False)
crypt=CryptContext(schemes=["bcrypt"], deprecated="auto")
config=Settings()

from .sso import router as sso_router
router.include_router(sso_router, prefix="/sso")

async def get_user(token: oauth=Depends()): # type: ignore
    token:Union[TokenDB,None]=await TokenDB.get_or_none(token=token).prefetch_related("user")
    if token is None:
        raise Forbidden()
    elif token.token_type != TokenType.bearer or timezone.now()>=token.expired_in or token.user is None:
        raise Forbidden()
    elif not token.user.is_verified:
        raise Forbidden(detail="Please verify email")
    else:
        return token.user

async def get_user_no_error(token: oauth_no_error=Depends()): # type: ignore
    if token is None:
        return None
    token:Union[TokenDB,None]=await TokenDB.get_or_none(token=token).prefetch_related("user")
    if token is None:
        return None
    elif token.token_type != TokenType.bearer or timezone.now()>=token.expired_in or token.user is None:
        return None
    else:
        return token.user

@router.post("/signin", response_model=Token)
async def signin(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), return_url:HttpUrl=config.DEFAULT_RETURN_URL):
    if HttpUrl(request.headers.get("origin", "")) not in config.AUTH_ALLOWED_ORIGINS and "application/json" not in request.headers.get("accept", ""):
        raise APIError (detail="Access Denied")
    user=await UserDB.get_or_none(Q(name=form_data.username) | Q(mail=form_data.username))
    if user is None:
        raise APIError(detail="Password or Username is wrong.")
    if user.password != "":
        if not crypt.verify(form_data.password,user.password):
            raise APIError(detail="Password or Username is wrong.")
        token=await TokenDB.create(token=secrets.token_hex(32), user=user, expired_in=timezone.now()+config.TOKEN_EXPIRE)
        if "users" not in request.session:
            request.session["users"]=[]
        request.session["users"].append({"name":user.name, "id":str(user.id), "token":token.token, "expired_in":token.expired_in.isoformat()})
        if return_url is not None and "application/json" not in request.headers.get("accept", ""):
            return RedirectResponse(str(return_url))
        return Token(access_token=token.token, token_type="bearer", user_id=user.id, expired_in=token.expired_in)
    else:
        raise APIError(detail="Password or Username is wrong.")

@router.post("/signup", response_model=bool)
async def signup(user:UserCreate, return_url:HttpUrl=config.DEFAULT_RETURN_URL):
    db_user, created=await UserDB.get_or_create({"name":user.mail, "display_name":"New User"},mail=user.mail)
    if not created:
        old_token = await db_user.tokens.filter(token_type=TokenType.mail_verify).first()
        if old_token:
            if old_token.expired_in < timezone.now():
                return False
            await old_token.delete()
    token=await TokenDB.create(token=secrets.token_hex(6), expired_in=timezone.now()+config.TOKEN_EXPIRE,
                               token_type=TokenType.mail_verify, user=db_user, return_url=return_url)
    msg=EmailMessage()
    msg['Subject'] = config.MAIL_VERIFY_SUBJECT
    msg['To'] = db_user.mail
    msg['From'] = "noreply@marusoftware.net"
    msg.set_content(f"Thank you for registration for {config.SERVICE_NAME}.\n"\
                    f"Please input following verification code: {token.token}")

    await mail.addMessage(msg)
    return True

@router.post("/signout")
async def signout(request:Request, token:str =Depends(oauth)):
    if "users" in request.session:
        request.session["users"]=[user for user in request.session["users"] if user["token"]!=token]
    await TokenDB.filter(token=token).delete()

@router.get("/session", response_model=List[Token])
async def session(request:Request):
    if not "users" in request.session:
        return []
    return [
        Token(access_token=user["token"], token_type="bearer", user_id=user["id"], expired_in=user["expired_in"]) 
        for user in request.session["users"] if await TokenDB.exists(token=user["token"], expired_in__gt=timezone.now())
        ]

@router.post("/callback", response_model=User)
async def callback(data:AuthCallbackData):
    if data.mail_token is None:
        raise Forbidden(detail="No infomation for authentication")
    token = await TokenDB.get_or_none(token=data.mail_token, token_type=TokenType.mail_verify).prefetch_related("user")
    if token is None:
        raise Forbidden(detail="Invalid token")
    user = token.user
    if user is None:
        raise Forbidden(detail="Invalid token")
    user.is_verified = True
    await user.save()
    await token.delete()
    return user