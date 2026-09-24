from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class CreationProduit(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=50)
    image: HttpUrl | None = Field(default=None, max_length=255)
    description: str = Field(max_length=500)
    category: str = Field(min_length=1, max_length=50)
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    is_available: bool = True
    restaurant_id: int = Field(gt=0)
    ingredients: list[str] = Field(default_factory=list)


class ModificationProduit(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=50)
    image: HttpUrl | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=500)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    price: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    is_available: bool | None = None
    restaurant_id: int | None = Field(default=None, gt=0)
    ingredients: list[str] | None = None


class DisponibiliteProduit(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_available: bool


class ProduitReponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    image: str | None
    description: str
    category: str
    price: Decimal
    is_available: bool
    restaurant_id: int
    ingredients: list[str]
