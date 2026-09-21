from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .admin import create_admin
from .db.config import settings
from .db.database import Base, SessionLocal, engine
from .models.restaurant import Restaurant  # noqa: F401
from .router import users

allow_origins = ["http://localhost:5173"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        create_admin(db, settings.admin_password)
    yield
    engine.dispose()

app = FastAPI(title="Ytasty Crousty API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(users.router, prefix="/users", tags=["user"])
