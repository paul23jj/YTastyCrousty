from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .admin import create_admin
from .db.config import settings
from .db.database import Base, SessionLocal, engine
from .models.restaurant import Restaurant
from .router import users
from .router import auth
from .router import products

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

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(products.router, prefix="/products", tags=["products"])
