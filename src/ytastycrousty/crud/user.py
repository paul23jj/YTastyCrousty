from ..security import hash_password
from ..models.user import User
from ..schemas.user import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(
        identifiant = user.identifiant,
        first_name = user.first_name,
        last_name = user.last_name,
        password = hashed_password,
        role = "client",
        status = "active",
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user