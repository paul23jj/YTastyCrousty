from pydantic import BaseModel, ConfigDict, Field

class RestaurantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    city: str
    address: str
    is_open: bool
    opening_hours: str
    contact: str

class RestaurantUpdate(BaseModel):
    name: str | None = None
    city: str | None = None
    address: str | None = None
    opening_hours: str | None = None
    contact: str | None = None


class AvailabilityUpdate(BaseModel):
    is_open: bool

class CreationRestaurant(BaseModel):
    name: str = Field(min_length=1)
    city: str = Field(min_length=1)
    address: str
    is_open: bool = True
    opening_hours: str
    contact: str
