from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
import contextlib, asyncio
from os.path import dirname

from .exceptions import APIError, Forbidden, NotFound
from .config import Settings
from .db import DB_CONFIG
from .mail import mail

from tortoise.contrib.fastapi import RegisterTortoise

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(app, config=DB_CONFIG, use_tz=True, timezone=settings.TZ):
        loop = asyncio.get_running_loop()
        mailtask=loop.create_task(mail._sendloop())
        yield
        mailtask.cancel()

def custom_generate_unique_id(route: APIRoute):
    return f"{f'{route.tags[0]}-'if len(route.tags) else ''}{route.name}"

app = FastAPI(
    title="at",
    description="at",
    version="0.0.1",
    root_path="/api/v1",
    generate_unique_id_function=custom_generate_unique_id,
    responses={400: {"model": APIError}, 
               401: {"model": Forbidden},
               404: {"model": NotFound}},
    lifespan=lifespan
)

@app.exception_handler(APIError)
async def api_error_handler(request: Request, error: APIError):
    raise HTTPException(error.status_code, detail=error.detail)

settings=Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*",],
    allow_credentials=True,
    allow_methods=["*",],
    allow_headers=["*",],
)

from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET)

from .routes import router
app.include_router(router)

app.mount("/static", StaticFiles(directory=dirname(__file__)+"/static"), name="static")