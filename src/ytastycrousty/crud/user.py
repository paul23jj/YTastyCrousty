from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user import UserCreate
from ..security import hash_password


def create_user(db: Session, user: UserCreate) -> User:
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
    db.commit()
    db.refresh(db_user)
    return db_user
