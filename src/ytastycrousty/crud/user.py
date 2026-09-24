from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models.user import User
from ..models.restaurant import Restaurant
from ..schemas.user import UserCreate
from ..security import hash_password


def create_user(db: Session, user: UserCreate) -> User:
    utilisateur = db.query(User).filter(User.username == user.username).first()
    if utilisateur is not None:
        raise HTTPException(status_code=400, detail="Cet identifiant est déjà utilisé")
    if user.role == "staff" and user.restaurant_id is None:
        raise HTTPException(status_code=400, detail="Un membre du staff doit avoir un restaurant")
    if user.restaurant_id is not None:
        if db.get(Restaurant, user.restaurant_id) is None:
            raise HTTPException(status_code=404, detail="Restaurant introuvable")
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        password=hashed_password,
        role=user.role,
        restaurant_id=user.restaurant_id,
    )
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Impossible de créer cet utilisateur")
    db.refresh(db_user)
    return db_user
