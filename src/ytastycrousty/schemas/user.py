from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str = Field(min_length=8, max_length=12, pattern=r"^[a-zA-Z0-9]+$")
    password: str = Field(min_length=12, max_length=64)
    role: Literal["admin", "staff", "direction"]
    restaurant_id: int | None = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not any(character.isdigit() for character in password):
            raise ValueError("Le mot de passe doit contenir au moins un chiffre")
        if not any(character.isupper() for character in password):
            raise ValueError("Le mot de passe doit contenir au moins une majuscule")
        if password.isalnum():
            raise ValueError("Le mot de passe doit contenir au moins un caractère spécial")
        return password


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    username: str
    role: str
    restaurant_id: int | None
