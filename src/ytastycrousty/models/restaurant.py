from sqlalchemy.orm import Mapped, mapped_column

from ..db.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    city: Mapped[str]
    address: Mapped[str]
    is_open: Mapped[bool]
    opening_hours: Mapped[str]
    contact: Mapped[str]
