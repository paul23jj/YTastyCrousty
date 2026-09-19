from passlib.context import CryptContext

pwd = CryptContext(schemes=["pbkdf2_sha256"])

def hash_password(password: str) -> str:
    return pwd.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    verif = pwd.verify(plain_password, hashed_password)
    return verif