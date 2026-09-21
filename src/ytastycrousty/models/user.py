from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    role: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    restaurant_id: Mapped[int | None] = mapped_column(
        ForeignKey("restaurants.id"), nullable=True
    )

