from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes import assistants
from app.routes import auth
from app.routes import threads
from app.routes import websockets
from .config import settings


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Lifespan event to initialize database connections and other activity that needs to happen before the application
    accepts its first request.
    """
    # uncomment this line if you intend on utilizing the MongoDB database for User credentials
    # await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(assistants.router)
app.include_router(threads.router)
app.include_router(websockets.router)


@app.get("/")
async def read_root():
    return dict(api=settings.API_NAME, version=settings.API_VERSION, author=settings.API_AUTHOR)
