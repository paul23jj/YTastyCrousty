from passlib.context import CryptContext
import jwt 
from datetime import timedelta
from datetime import timezone 
from datetime import datetime
from .db.config import settings

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