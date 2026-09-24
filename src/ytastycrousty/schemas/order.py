from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    
class OrderItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    
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
    unit_price: Decimal
    
class CustomerOut(BaseModel):
    name: str
    email: EmailStr
    
class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_number: str
    restaurant_id: int
    created_at: datetime
    items: list[OrderItemOut]
    total_price: Decimal
    status: str
    pickup_mode: str
    customer: CustomerOut