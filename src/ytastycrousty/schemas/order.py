from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    
class OrderItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=2147483647, strict=True)
    
class OrderCreate(BaseModel):
    restaurant_id: int = Field(gt=0)
    items: list[OrderItemCreate] = Field(min_length=1)
    pickup_mode: Literal["onsite", "takeaway"]
    customer: CustomerCreate
    
class OrderStatusUpdate(BaseModel):
    status: Literal[
        "pending",
        "validated",
        "preparing",
        "ready",
        "collected",
        "cancelled",
    ]
    
class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    product_id: int
    quantity: int
    unit_price: float
    
class CustomerOut(BaseModel):
    name: str
    email: str
    
class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_number: str
    restaurant_id: int
    created_at: datetime
    items: list[OrderItemOut]
    total_price: float
    status: str
    pickup_mode: str
    customer: CustomerOut
