from passlib.context import CryptContext
import jwt 
from datetime import timedelta
from datetime import timezone 
from datetime import datetime
from .db.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from .db.database import get_db
from .models.user import User

pwd = CryptContext(schemes=["pbkdf2_sha256"])


def hash_password(password: str) -> str:
    return pwd.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    verif = pwd.verify(plain_password, hashed_password)
    return verif

def creer_token(user_id:int,role:str,restaurant_id:int|None):
    dureeToken = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    ContenuToken = {
        "sub": str(user_id),
        "role": role,
        "restaurant_id": restaurant_id,
        "exp": dureeToken
    }
    
    token = jwt.encode(ContenuToken,settings.secret_key,algorithm=settings.algorithm)
    return token


bearer = HTTPBearer(auto_error=False)


def recuperer_utilisateur(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentification requise ou token invalide",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"require": ["sub", "exp"]},
        )
        user_id = int(payload["sub"])
        if user_id <= 0 or user_id > 2147483647:
            raise ValueError("Identifiant invalide")
    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise unauthorized from None

    user = db.get(User, user_id)
    if user is None:
        raise unauthorized
    return user


def verifier_admin(user: User = Depends(recuperer_utilisateur)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    return user


def verifier_droits_produit(user: User = Depends(recuperer_utilisateur)) -> User:
    if user.role not in {"admin", "staff"}:
        raise HTTPException(status_code=403, detail="Modification des produits interdite")
    return user


def verifier_droits_restaurant(user: User, restaurant_id: int) -> None:
    if user.role != "admin" and user.restaurant_id != restaurant_id:
        raise HTTPException(status_code=403, detail="Accès interdit à ce restaurant")
