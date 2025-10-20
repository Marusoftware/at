from email.message import EmailMessage
from typing import Annotated, List, Optional, Union
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, Depends, Request
import secrets
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from pydantic import HttpUrl, ValidationError
from tortoise.expressions import Q
from tortoise import timezone
from os.path import dirname

from ..mail import mail
from ..exceptions import APIError, Forbidden
from ..models.response.user import User, Token
from ..models.request.auth import UserCreate
from ..models.db.user import TokenType
from ..models.db import User as UserDB, Token as TokenDB
from ..config import Settings

router=APIRouter(tags=["Auth"])
oauth=OAuth2PasswordBearer(tokenUrl="/auth/signin")
oauth_no_error=OAuth2PasswordBearer(tokenUrl="/auth/signin", auto_error=False)
crypt=CryptContext(schemes=["bcrypt"], deprecated="auto")
config=Settings()
templates = Jinja2Templates(directory=dirname(__file__)+"/../templates")

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

@router.get("/signin", response_class=HTMLResponse)
async def signin_html(request:Request, return_url:HttpUrl=config.DEFAULT_RETURN_URL):
    return templates.TemplateResponse(
        request=request, name="signin/index.html", context={"return_url":return_url}
    )

def show_signin_error(request:Request, return_url:HttpUrl):
    if "application/json" in request.headers.get("accept", ""):
        raise APIError(detail="Password or Username is wrong.")
    else:
        return templates.TemplateResponse(
            request=request, name="signin/index.html", context={"return_url":str(return_url), "error":"Password or Username is wrong."}
        )

@router.post("/signin", response_model=Token)
async def signin(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), return_url:HttpUrl=config.DEFAULT_RETURN_URL):
    user=await UserDB.get_or_none(Q(name=form_data.username) | Q(mail=form_data.username))
    if user is None:
        return show_signin_error(request, return_url)
    if user.password != "":
        if not crypt.verify(form_data.password,user.password):
            return show_signin_error(request, return_url)
        token=await TokenDB.create(token=secrets.token_hex(32), user=user, expired_in=timezone.now()+config.TOKEN_EXPIRE)
        if "users" not in request.session:
            request.session["users"]=[]
        request.session["users"].append({"name":user.name, "id":str(user.id), "token":token.token, "expired_in":token.expired_in.isoformat()})
        if return_url is not None and "application/json" not in request.headers.get("accept", ""):
            return RedirectResponse(str(return_url))
        return Token(access_token=token.token, token_type="bearer", user_id=user.id, expired_in=token.expired_in)
    else:
        return show_signin_error(request, return_url)

def show_signup_error(request:Request, return_url:HttpUrl):
    if "application/json" in request.headers.get("accept", ""):
        raise APIError(detail="Password or Username is wrong.")
    else:
        return templates.TemplateResponse(
            request=request, name="signup/index.html", context={"return_url":str(return_url), "error":"Password or Username is wrong."}
        )

@router.get("/signup", response_class=HTMLResponse)
async def signup_html(request:Request, return_url:HttpUrl=config.DEFAULT_RETURN_URL):
    return templates.TemplateResponse(
        request=request, name="signup/index.html", context={"return_url":str(return_url)}
    )

@router.post("/signup", response_model=User, openapi_extra={"requestBody":{"content":{
    "application/x-www-form-urlencoded": {"schema":UserCreate.model_json_schema()},
    "application/json": {"schema":UserCreate.model_json_schema()}
}}})
async def signup(request:Request, return_url:HttpUrl=config.DEFAULT_RETURN_URL):
    try:
        if "application/json" in request.headers.get("content-type", ""):
            user=UserCreate.model_validate(await request.json())
        else:
            user=UserCreate.model_validate(await request.form())
    except ValidationError:
        return show_signup_error(request, return_url)
    if await UserDB.exists(Q(name=user.name) | Q(mail=user.mail)):
        return show_signup_error(request, return_url)
    db_user=await UserDB.create(name=user.name, mail=user.mail, password=crypt.hash(user.password.get_secret_value()))
    token=await TokenDB.create(token=secrets.token_hex(10), expired_in=timezone.now()+config.TOKEN_EXPIRE,
                               token_type=TokenType.mail_verify, user=db_user, return_url=return_url)
    msg=EmailMessage()
    msg['Subject'] = "Marusoftware: Email Verification"
    msg['To'] = db_user.mail
    msg['From'] = "noreply@marusoftware.net"
    msg.preamble="Thank you for registration for @Marusoftware.\n"\
                f"{config.CALLBACK_URL}?mail_token={token.token}"
    await mail.addMessage(msg)
    if "application/json" in request.headers.get("accept",""):
        return db_user
    else:
        return templates.TemplateResponse(
            request=request, name="signup/success.html", context={"return_url":str(return_url),"user":db_user}
        )

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

@router.get("/callback")
async def callback(request:Request, mail_token:Optional[str]=None):
    if mail_token is None:
        raise Forbidden(detail="No infomation for authentication")
    token = await TokenDB.get_or_none(token=mail_token, token_type=TokenType.mail_verify).prefetch_related("user")
    if token is None:
        raise Forbidden(detail="Invalid token")
    user = token.user
    if user is None:
        raise Forbidden(detail="Invalid token")
    user.is_verified = True
    await user.save()
    return_url=token.return_url
    await token.delete()
    return templates.TemplateResponse(
            request=request, name="callback/success.html", context={"return_url":return_url, "user":user}
        )