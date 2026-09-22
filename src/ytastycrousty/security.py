from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt

from .db.config import settings

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

pwd = CryptContext(schemes=["pbkdf2_sha256"])

def hash_password(password: str) -> str:
    return pwd.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    verif = pwd.verify(plain_password, hashed_password)
    return verif

